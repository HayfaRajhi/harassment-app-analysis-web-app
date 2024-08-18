import json
import re
from detoxify import Detoxify


## function to clean comment and post description cleaning (deleting emojis and unspecied caracters)
def clean_text(comment_text):
      # Replace sequences of multiple newline characters with a single space
     cleaned_text = re.sub(r'\n+', ' ', comment_text)# Remove extra spaces
     cleaned_text  = re.sub(r'[^\w\s]', '', cleaned_text) # regular expression of emojis(matches any character that is not a word character (\w) or whitespace character (\s).) # Remove special characters

     # Return None if the cleaned text is empty
     return cleaned_text.lower() if cleaned_text.strip() else None


# Function to filter posts related to child harassment
def is_child_harassment(text):
    if text is None:
        return False
    # Define keywords related to child harassment
    keywords = ['child', 'children', 'harassment', 'abuse', 'exploitation','minor','kid','underage']
    # Check if any keyword is in the text
    return any(keyword in text.lower() for keyword in keywords)




def is_harrasment_related(text):
    if text is None:
        return False
    #Define keywords related to child harassment

    harassment_keywords = {'child', 'children', 'harassment', 'abuse', 'exploitation'}
    # Tokenize the text into words
    words= set(text.lower().split())
    # Check for any overlap between harassment keywords and words in the text
    keyword_match = harassment_keywords.intersection(words)

 # Perform toxicity analysis using Detoxify
    toxicity_scores = Detoxify('original').predict(text)
    toxicity = toxicity_scores.get('toxicity', 0)

    # Define thresholds for harassment-related content
    keyword_threshold = 1  # At least 1 harassment keyword
    toxicity_threshold = 0.5  # Adjust this threshold based on your use case

    # Determine if the post is harassment-related based on keyword match and toxicity score
    return len(keyword_match) >= keyword_threshold or toxicity >= toxicity_threshold


from sentence_transformers import SentenceTransformer, util

# Load a pre-trained model
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Predefined harassment-related sentences (can be expanded)
harassment_sentences = [
    "This post is about child abuse.",
    "This is a case of bullying.",
    "The content involves exploitation of a minor."
]
harassment_embeddings = model.encode(harassment_sentences, convert_to_tensor=True)

def is_harassment_related_semantic(text):
    if text is None:
        return False
    
    text_embedding = model.encode(text, convert_to_tensor=True)
    cosine_scores = util.pytorch_cos_sim(text_embedding, harassment_embeddings)
    
    # Threshold for considering the text as related to harassment (adjust as needed)
    threshold = 0.5
    
    return cosine_scores.max() > threshold
