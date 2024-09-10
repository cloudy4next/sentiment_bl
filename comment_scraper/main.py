
from comment import Comment
import os
import requests
import time
from dotenv import load_dotenv
from bus import publish, connect
from fetched_cooments import load_processed_ids, save_processed_id

load_dotenv()

ACCESS_TOKEN = os.getenv('FACEBOOK_ACCESS_TOKEN')
POST_ID = os.getenv('POST_ID')
RABBITMQ_HOST = os.getenv('RABBITHOST', 'localhost')

connection = connect(RABBITMQ_HOST)
channel = connection.channel()
    
def fetch_last_comment():
    comments_url = f'https://graph.facebook.com/v20.0/{POST_ID}/comments'
    comments_params = {
        'access_token': ACCESS_TOKEN, 
        'fields': 'message,from,created_time',
        'limit': 100  
    }
    comments_response = requests.get(comments_url, params=comments_params)    
    comments = comments_response.json().get('data', [])
    print(comments)
    if comments: 
        latest_comment = comments[-1]
        comment_message = latest_comment.get('message', '')
        commenter_name = latest_comment.get('from', {}).get('name', 'Unknown')
        commenter_id = latest_comment.get('from', {}).get('id', 'Unknown')
        comment_time = latest_comment.get('created_time', '')
        comment_id = latest_comment.get('id', '')
        
        processed_ids = load_processed_ids()
        if comment_id not in processed_ids:      
            comment_obj = Comment(
                user_name=commenter_name,
                user_id=commenter_id,
                comment=comment_message,
                time=comment_time,
                fb_comment_id=comment_id
            )   
            print("Found new comment :: ", comment_obj)
            publish(queue='comments', body=comment_obj,channel=channel)
            save_processed_id(comment_id)
        else:
            print("No new comments found.")
    else:
        print("No comments found.")

if __name__ == "__main__":
    
    while True:
        fetch_last_comment()
        time.sleep(15)
