
import os
from dotenv import load_dotenv


load_dotenv()



FILE_NAME = os.getenv('PROCESSED_COMMENTS_FILE')
PROCESSED_COMMENTS_FILE = os.path.join(os.getcwd(), FILE_NAME)


def ensure_file_exists(file_path):
    print(f"Ensuring file exists: {file_path}")

    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"Created directory: {directory}")
        except Exception as e:
            print(f"Error creating directory: {e}")
            raise

    if not os.path.isfile(file_path):
        try:
            with open(file_path, 'w') as file:
                pass  
            print(f"Created file: {file_path}")
        except Exception as e:
            print(f"Error creating file: {e}")
            raise

def load_processed_ids():
    ensure_file_exists(PROCESSED_COMMENTS_FILE)
    try:
        with open(PROCESSED_COMMENTS_FILE, 'r') as file:
            return set(line.strip() for line in file)
    except Exception as e:
        print(f"Error loading processed IDs: {e}")
        raise

def save_processed_id(comment_id):
    ensure_file_exists(PROCESSED_COMMENTS_FILE)
    try:
        with open(PROCESSED_COMMENTS_FILE, 'a') as file:
            file.write(f"{comment_id}\n")
        print(f"Saved comment ID: {comment_id}")
    except Exception as e:
        print(f"Error saving comment ID: {e}")
        raise
    