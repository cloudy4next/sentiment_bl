import os
import openai
import pickle
from dataclasses import dataclass
from bus import consume, publish, connect, declare
from dotenv import load_dotenv
from comment import Comment
load_dotenv()
from processed_comment import ProcessedComment
from category_manager import CategoryManager
import re


openai.api_key = os.getenv('OPENAI_API_KEY')


RABBITHOST = os.getenv('RABBITHOST', 'localhost')
PROCESSED_QUEUE = 'processed_comment'


def analyze_text(text):
    categories_list = CategoryManager.get_categories()
    messages = [
        {"role": "system", "content": "You are an assistant that helps categorize and analyze text."},
        {"role": "user", "content": f"Analyze the following text for sentiment and categorize it into one of the provided categories and subcategories.\n\nText: \"{text}\"\n\nCategories:\n{categories_list}\n\nPlease provide the sentiment (positive, negative, neutral) and the category and subcategory of the text."}
    ]
    
    response = openai.ChatCompletion.create(
        model=os.getenv('OPENAI_MODEL'),
        messages=messages,
        max_tokens=150,
        temperature=0.7
    )
        
    return response.choices[0].message['content']

def parse_analysis_result(result_str):
    sentiment_match = re.search(r'Sentiment:\s*(\w+)', result_str)
    category_match = re.search(r'Category:\s*([A-Za-z\s/]+)', result_str)
    subcategory_match = re.search(r'Subcategory:\s*(.+)', result_str)
    
    # Extract values
    sentiment = sentiment_match.group(1) if sentiment_match else None
    category = category_match.group(1) if category_match else None
    subcategory = subcategory_match.group(1) if subcategory_match else None
    
    return sentiment, category, subcategory



def process_comment(ch, method, properties, body):
    comment = pickle.loads(body)
    text = comment.message
    
    response = analyze_text(text)
    sentiment, category, sub_category = parse_analysis_result(response)

    processed_comment = ProcessedComment(
        fb_comment_id=comment.fb_comment_id,
        sentiment=sentiment,
        category=category,
        sub_category=sub_category
    )
    
    publish(PROCESSED_QUEUE, processed_comment, channel)

if __name__ == "__main__":
    connection = connect(RABBITHOST)
    while not connection:
        connection = connect(RABBITHOST)

    channel = connection.channel()
    channel.basic_qos(prefetch_count=1)
    
    declare([PROCESSED_QUEUE], channel)

    consume(queue='comments', callback=process_comment, channel=channel)
