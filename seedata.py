from pymongo import MongoClient
import json

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['harassment_analytics']  
collection = db['posts']  

        # Query all data from the 'posts' collection
posts = list(collection.find({}))

        # Convert ObjectId to string
for post in posts:
            post['_id'] = str(post['_id'])
            print(post)
  # Specify the file path
file_path = './posts.json'

        # Write the data to a JSON file
with open(file_path, 'w') as json_file:
            json.dump(posts, json_file, indent=4)