from flask import Flask, jsonify, request, render_template, redirect, url_for, send_file
import json
import os
from pymongo import MongoClient
from utils_ETL import clean_text, is_child_harassment,is_harrasment_related,is_harassment_related_semantic
from detoxify import Detoxify
from werkzeug.utils import secure_filename
from bson import ObjectId

app = Flask(__name__)
app.secret_key = "app"

# Initialize Detoxify model
detoxify_model = Detoxify('original')

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['harassment_analytics']
collection = db['posts']

# HTML Upload Form
@app.route('/')
def upload_form():
    return render_template('upload.html')

# Convert MongoDB ObjectId to string
def objectid_to_str(data):
    if isinstance(data, ObjectId):
        return str(data)
    elif isinstance(data, dict):
        return {k: objectid_to_str(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [objectid_to_str(i) for i in data]
    return data

# Handle File Upload and ETL Process
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    if file:
        # Define the directory and make sure it exists
        tmp_dir = os.path.join(os.getcwd(), 'tmp')
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(tmp_dir, filename)
        file.save(filepath)
        
        try:
            # Load JSON data from file
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            return f"Error reading file: {e}", 400
        
        cleaned_data = []
        for post in data:
            post['post_text'] = clean_text(post['post_text'])
            cleaned_comments = []
            for comment in post['comments']:
                cleaned_comment_text = clean_text(comment['comment_text'])
                if cleaned_comment_text:
                    cleaned_comments.append({
                        'user_name': comment['user_name'],
                        'comment_text': cleaned_comment_text
                    })
            post['comments'] = cleaned_comments
            if  is_child_harassment(post['post_text']):
                cleaned_data.append(post)

        for post in cleaned_data:
            analysis = analyze_toxicity(post['post_text'])
            post['toxicity_analysis'] = float(analysis.get('toxicity', 0))
            for comment in post['comments']:
                toxicity_scores = analyze_toxicity(comment['comment_text'])
                comment['toxicity'] = float(toxicity_scores.get('toxicity', 0))
        
        try:
            result = collection.insert_many(cleaned_data)
            inserted_ids = [str(id) for id in result.inserted_ids]
        except Exception as e:
            return f"Error inserting data into MongoDB: {e}", 500
        
        return redirect(url_for('view_data'))

# View Stored Data
@app.route('/data', methods=['GET'])
def view_data():
    analyzed_data = list(collection.find({}, {'_id': 0}))
    return render_template('data.html', analyzed_data=analyzed_data)



# Download Data as JSON
@app.route('/download', methods=['GET'])
def download_data():
    analyzed_data = list(collection.find({}, {'_id': 0}))
    tmp_dir = os.path.join(os.getcwd(), 'tmp')
    download_path = os.path.join(tmp_dir, 'analyzed_data.json')
    
    try:
        with open(download_path, 'w', encoding='utf-8') as f:
            json.dump(analyzed_data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        return f"Error saving file: {e}", 500
    
    return send_file(download_path, as_attachment=True)

# Function to analyze toxicity using Detoxify
def analyze_toxicity(text):
    results = detoxify_model.predict(text)
    return results

if __name__ == '__main__':
    app.run(debug=True)
