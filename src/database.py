import re
import os
from typing import Optional, Any, Dict, List
import pymongo
from pymongo.server_api import ServerApi
from pymongo.collection import Collection
from pymongo.results import DeleteResult, UpdateResult
from dotenv import load_dotenv


class MongoDatabase:
    def __init__(self, collection_name="botdata", database_name=None):
        load_dotenv()
        
        # Try multiple environment variable names for compatibility
        self.mongo_uri = (
            os.getenv("MONGODB_URI") or 
            os.getenv("MONGO_URI") or
            os.getenv("mongodb_uri")
        )
        
        if not self.mongo_uri:
            print("❌ MongoDB URI not found in environment variables")
            print("🔍 Available MongoDB-related environment variables:")
            for key in sorted(os.environ.keys()):
                if any(term in key.lower() for term in ['mongo', 'uri', 'database']):
                    value = os.getenv(key)
                    if value:
                        # Show first 50 chars for debugging, hide sensitive parts
                        display_value = value[:50] + "..." if len(value) > 50 else value
                        if 'password' in key.lower() or 'secret' in key.lower():
                            display_value = "*" * min(len(value), 10)
                        print(f"   {key}: {display_value}")
            raise ValueError("MongoDB URI not found. Expected: MONGODB_URI, MONGO_URI, or mongodb_uri")
        
        self.database_name = (
            database_name or 
            os.getenv("MONGODB_DATABASE") or 
            os.getenv("MONGO_DATABASE") or
            "botchuot"
        )
        self.collection_name = collection_name
        self.client: Optional[pymongo.MongoClient] = None
        self.collection: Optional[Collection] = None
        self.is_loaded = False
    
    def load(self):
        try:
            self.client = pymongo.MongoClient(self.mongo_uri, server_api=ServerApi('1'))
            self.client.admin.command('ping')
            self.collection = self.client[self.database_name][self.collection_name]
            self.is_loaded = True
            return True
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            return False
    
    def get(self, key) -> Optional[Dict[str, Any]]:
        if not self.is_loaded: 
            self.load()
        if self.collection is None:
            raise RuntimeError("Database collection not initialized")
        return self.collection.find_one({"_id": str(key)})
    
    def set(self, key, value) -> UpdateResult:
        if not self.is_loaded: 
            self.load()
        if self.collection is None:
            raise RuntimeError("Database collection not initialized")
        data = value if isinstance(value, dict) else {"value": value}
        data["_id"] = str(key)
        return self.collection.replace_one({"_id": str(key)}, data, upsert=True)
    
    def delete(self, key) -> DeleteResult:
        if not self.is_loaded: 
            self.load()
        if self.collection is None:
            raise RuntimeError("Database collection not initialized")
        return self.collection.delete_one({"_id": str(key)})
    
    def search(self, query) -> List[Dict[str, Any]]:
        if not self.is_loaded: 
            self.load()
        if self.collection is None:
            raise RuntimeError("Database collection not initialized")
        pattern = re.compile(f".*{re.escape(query)}.*", re.IGNORECASE)
        results = []
        for doc in self.collection.find():
            if any(isinstance(v, str) and re.search(pattern, v) for v in doc.values()):
                results.append(doc)
        return results
    
    def find(self, query_dict) -> List[Dict[str, Any]]:
        if not self.is_loaded: 
            self.load()
        if self.collection is None:
            raise RuntimeError("Database collection not initialized")
        return list(self.collection.find(query_dict))
    
    def close(self):
        if self.client:
            self.client.close()
            self.is_loaded = False
