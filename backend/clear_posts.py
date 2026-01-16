
import os
import sys
from dotenv import load_dotenv
from pymongo import MongoClient

# Ensure project root is in path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '.'))
sys.path.insert(0, project_root)

# Load env
load_dotenv(os.path.join(project_root, "../.env"))

def fix_data():
    mongo_url = "mongodb://localhost:27017/instaintelli"
    client = MongoClient(mongo_url)
    db = client["instaintelli"]
    collection = db["posts"]
    
    count = collection.count_documents({})
    print(f"Current posts: {count}")
    
    # Delete all posts to start fresh
    collection.delete_many({})
    print("Cleared all posts.")
    
    client.close()

if __name__ == "__main__":
    fix_data()
