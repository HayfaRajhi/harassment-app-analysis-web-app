import json
import re
from detoxify import Detoxify


## function to clean comment and post description cleaning (deleting emojis and unspecied caracters)
def clean_text(comment_text):
      # Replace sequences of multiple newline characters with a single space
     cleaned_text = re.sub(r'\n+', ' ', comment_text)
     cleaned_text  = re.sub(r'[^\w\s]', '', cleaned_text) # regular expression of emojis(matches any character that is not a word character (\w) or whitespace character (\s).)

     # Return None if the cleaned text is empty
     return cleaned_text if cleaned_text.strip() else None


# Function to filter posts related to child harassment
def is_child_harassment(text):
    # Define keywords related to child harassment
    keywords = ['child', 'children', 'harassment', 'abuse', 'exploitation']
    # Check if any keyword is in the text
    return any(keyword in text.lower() for keyword in keywords)



