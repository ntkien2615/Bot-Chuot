import re
import pymongo
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv


class MongoDatabase:
    def __init__(self, collection_name="botdata", database_name=None):
        load_dotenv()
        self.mongo_uri = os.getenv("MONGODB_URI")
        if not self.mongo_uri:
            raise ValueError("MONGODB_URI environment variable not set")
        
        self.database_name = database_name or os.getenv("MONGODB_DATABASE", "botchuot")
        self.collection_name = collection_name
        self.client = None
        self.collection = None
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
    
    def get(self, key):
        if not self.is_loaded: 
            self.load()
        return self.collection.find_one({"_id": str(key)})
    
    def set(self, key, value):
        if not self.is_loaded: 
            self.load()
        data = value if isinstance(value, dict) else {"value": value}
        data["_id"] = str(key)
        return self.collection.replace_one({"_id": str(key)}, data, upsert=True)
    
    def delete(self, key):
        if not self.is_loaded: 
            self.load()
        return self.collection.delete_one({"_id": str(key)})
    
    def search(self, query):
        if not self.is_loaded: 
            self.load()
        pattern = re.compile(f".*{re.escape(query)}.*", re.IGNORECASE)
        results = []
        for doc in self.collection.find():
            if any(isinstance(v, str) and re.search(pattern, v) for v in doc.values()):
                results.append(doc)
        return results
    
    def find(self, query_dict):
        if not self.is_loaded: 
            self.load()
        return list(self.collection.find(query_dict))
    
    def close(self):
        if self.client:
            self.client.close()
            self.is_loaded = False
