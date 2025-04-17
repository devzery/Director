import os
import videodb
from dotenv import load_dotenv

load_dotenv()

def connect_to_videodb_dev():
    """
    Connect to the VideoDB server.
    
    Returns:
        videodb.VideoDB: The connected VideoDB instance.
    """
    api_key = os.getenv("VIDEO_DB_API_KEY")
    if not api_key:
        raise ValueError("API key not found in environment variables.")
    try:
        # Assuming videodb has a method to connect
        conn = videodb.connect(api_key=api_key)
        return conn
    except Exception as e:
        print(f"Error connecting to VideoDB: {e}")
        return None

def connect_to_videodb():
    """
    Connect to the VideoDB server.
    
    Returns:
        videodb.VideoDB: The connected VideoDB instance.
    """
    api_key = os.getenv("VIDEO_DB_API_KEY_DEV")
    try:
        # Assuming videodb has a method to connect
        conn = videodb.connect(api_key=api_key, base_url="https://api.dev.videodb.io")
        return conn
    except Exception as e:
        print(f"Error connecting to VideoDB: {e}")
        return None

def find_collections(conn):
    """
    Find all collections in the VideoDB server.
    
    Returns:
        list: A list of collection names.
    """
    collections = []
    try:
        # Assuming videodb has a method to get collections
        collections = conn.get_collections()
    except Exception as e:
        print(f"Error fetching collections: {e}")
    
    return collections
