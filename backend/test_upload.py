
import requests
import os
from dotenv import load_dotenv

load_dotenv("../.env")

def test_upload():
    url = "http://localhost:8000/api/v1/posts/upload"
    
    # We need a dummy image file
    with open("test_image.jpg", "wb") as f:
        f.write(b"fake image data")
        
    files = {
        'file': ('test_image.jpg', open('test_image.jpg', 'rb'), 'image/jpeg')
    }
    
    data = {
        'user_id': 'user_123',
        'text': 'Test post from script'
    }
    
    try:
        response = requests.post(url, files=files, data=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if os.path.exists("test_image.jpg"):
            os.remove("test_image.jpg")

if __name__ == "__main__":
    test_upload()
