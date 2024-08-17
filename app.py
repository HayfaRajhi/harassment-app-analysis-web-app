from flask import Flask, jsonify, request , render_template ,redirect
import json
import re
from pymongo import MongoClient
from utils_ETL import clean_text ,is_child_harassment
from detoxify import Detoxify


# Function to analyze toxicity using Detoxify
def analyze_toxicity(text):
    # Use Detoxify to get toxicity scores
    results = detoxify_model.predict(text)
    return results

app = Flask(__name__)

# Initialize Detoxify model
detoxify_model = Detoxify('original')

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['harassment_analytics']  
collection = db['posts']  

@app.route('/clean-filter', methods=['POST'])
def clean_filter_data():
    try:
        data = request.get_json()
        cleaned_data = []

        for post in data:
            # Clean post text
            post['post_text'] = clean_text(post['post_text']) 
            
            # Clean and filter comments
            cleaned_comments = []
            for comment in post['comments']:
                cleaned_comment_text = clean_text(comment['comment_text'])
                # Keep only non-empty comments
                if cleaned_comment_text is not None:
                    cleaned_comments.append({
                        'user_name': comment['user_name'],
                        'comment_text': cleaned_comment_text
                    })
            
            post['comments'] = cleaned_comments
            
            # Filter posts
            if not is_child_harassment(post['post_text']):
                cleaned_data.append(post)  # Correct indentation
            
        # Analyze toxicity for cleaned comments
        for post in cleaned_data:
            for comment in post['comments']:
 # Get the 'toxicity' score from the result dictionary
                toxicity_scores = analyze_toxicity(comment['comment_text'])
                comment['toxicity'] = float(toxicity_scores.get('toxicity', 0))
        # Insert cleaned and analyzed data into MongoDB
        result = collection.insert_many(cleaned_data)
         # Convert ObjectId to string for JSON serialization
        inserted_ids = [str(id) for id in result.inserted_ids]
        print(result)
        return jsonify({'message': 'Data stored in MongoDB successfully', 'inserted_ids': inserted_ids}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Optional: Removing or placing the code within a route
# posts_d = db['posts'].find({})
# for dt in posts_d: 
#          print(dt) 

if __name__ == '__main__':
    app.run(debug=True)
