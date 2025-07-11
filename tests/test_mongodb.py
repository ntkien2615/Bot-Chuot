import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

def test_mongodb_connection():
    """Test connection to MongoDB Atlas."""
    # Load environment variables
    load_dotenv()
    
    # Get MongoDB URI from environment variables
    uri = os.getenv("MONGODB_URI")
    
    if not uri:
        print("Error: MONGODB_URI environment variable not set.")
        print("Please create a .env file with your MongoDB connection string.")
        print("Example: MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority")
        return False
    
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        
        # Try to access the database and collection
        db_name = os.getenv("MONGODB_DATABASE", "botchuot")
        collection_name = "test_collection"
        
        db = client[db_name]
        collection = db[collection_name]
        
        # Insert a test document
        result = collection.insert_one({"test": "connection"})
        print(f"Inserted document with ID: {result.inserted_id}")
        
        # Find the document
        document = collection.find_one({"test": "connection"})
        print(f"Found document: {document}")
        
        # Clean up - delete the test document
        collection.delete_one({"_id": result.inserted_id})
        print("Test document deleted")
        
        client.close()
        return True
    except Exception as e:
        print(f"MongoDB connection error: {e}")
        return False

if __name__ == "__main__":
    test_mongodb_connection()