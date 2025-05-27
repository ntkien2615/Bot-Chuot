import re
from abc import ABC, abstractmethod
import pymongo
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv


class Database(ABC):
    """Abstract base class for all database types."""
    
    def __init__(self, database_path=None):
        self.database_path = database_path
        self.is_loaded = False
    
    @abstractmethod
    def load(self):
        """Load data from the database source."""
        pass
    
    @abstractmethod
    def save(self):
        """Save data to the database source."""
        pass
    
    @abstractmethod
    def get(self, key):
        """Get a value by key."""
        pass
    
    @abstractmethod
    def search(self, query):
        """Search for entries in the database."""
        pass


class FileDatabase(Database):
    """Base class for file-based databases."""
    
    def __init__(self, file_path):
        super().__init__(file_path)
        self.data = {}
    
    def load(self):
        """Load data from file."""
        try:
            with open(self.database_path, 'r', encoding='utf-8') as f:
                self._parse_file_content(f.readlines())
            self.is_loaded = True
            return True
        except Exception as e:
            print(f"Error loading database: {e}")
            self.is_loaded = False
            return False
    
    def save(self):
        """Save data to file."""
        try:
            with open(self.database_path, 'w', encoding='utf-8') as f:
                f.write(self._format_data_for_save())
            return True
        except Exception as e:
            print(f"Error saving database: {e}")
            return False
    
    def get(self, key):
        """Get a value by key."""
        return self.data.get(str(key))
    
    def search(self, query):
        """Search for entries in the database."""
        query = query.lower()
        return {k: v for k, v in self.data.items() if query in str(v).lower()}
    
    @abstractmethod
    def _parse_file_content(self, lines):
        """Parse the content of the file."""
        pass
    
    @abstractmethod
    def _format_data_for_save(self):
        """Format the data for saving to file."""
        pass


class MongoDatabase(Database):
    """Database implementation for MongoDB."""
    
    def __init__(self, collection_name="botdata", database_name=None):
        super().__init__()
        load_dotenv()
        self.mongo_uri = os.getenv("MONGODB_URI")
        if not self.mongo_uri:
            raise ValueError("MONGODB_URI environment variable not set")
        
        # Use environment variable for database name if not provided
        if database_name is None:
            database_name = os.getenv("MONGODB_DATABASE", "botchuot")
        
        self.client = None
        self.db = None
        self.collection = None
        self.database_name = database_name
        self.collection_name = collection_name
        self.is_loaded = False
    
    def load(self):
        """Connect to MongoDB and load collection."""
        try:
            # Create a new client and connect to the server using Server API version 1
            self.client = pymongo.MongoClient(self.mongo_uri, server_api=ServerApi('1'))
            
            # Send a ping to confirm a successful connection
            self.client.admin.command('ping')
            print("Successfully connected to MongoDB Atlas!")
            
            self.db = self.client[self.database_name]
            self.collection = self.db[self.collection_name]
            self.is_loaded = True
            return True
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            self.is_loaded = False
            return False
    
    def save(self):
        """Not used for MongoDB as changes are saved directly via insert/update methods."""
        return True
    
    def get(self, key):
        """Get a document by its _id field."""
        if not self.is_loaded:
            self.load()
        return self.collection.find_one({"_id": str(key)})
    
    def set(self, key, value):
        """Insert or update a document."""
        if not self.is_loaded:
            self.load()
            
        data = value
        if isinstance(data, dict):
            data["_id"] = str(key)
        else:
            data = {"_id": str(key), "value": value}
            
        return self.collection.replace_one(
            {"_id": str(key)}, 
            data, 
            upsert=True
        )
    
    def delete(self, key):
        """Delete a document by its _id field."""
        if not self.is_loaded:
            self.load()
        return self.collection.delete_one({"_id": str(key)})
    
    def search(self, query):
        """Search for documents containing the query in any field."""
        if not self.is_loaded:
            self.load()
        
        # Convert query to regex pattern
        pattern = re.compile(f".*{re.escape(query)}.*", re.IGNORECASE)
        
        # For simpler search, just search in all string fields
        results = []
        for doc in self.collection.find():
            for key, value in doc.items():
                if isinstance(value, str) and re.search(pattern, value):
                    results.append(doc)
                    break
        
        return results
    
    def find(self, query_dict):
        """Find documents matching the query dictionary."""
        if not self.is_loaded:
            self.load()
        return list(self.collection.find(query_dict))
    
    def insert_many(self, documents):
        """Insert multiple documents."""
        if not self.is_loaded:
            self.load()
        return self.collection.insert_many(documents)
    
    def close(self):
        """Close the MongoDB connection."""
        if self.client:
            self.client.close()
            self.is_loaded = False


class RuleDatabase(FileDatabase):
    """Database for internet rules."""
    
    def __init__(self, file_path='txt_files/100_rules_of_internet.txt'):
        super().__init__(file_path)
        self.load()  # Automatically load rules when initialized
    
    def _parse_file_content(self, lines):
        """Parse the rules file content."""
        self.data = {}
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            rule_num = self._parse_rule_number(line)
            if rule_num:
                content = self._get_rule_content(line)
                if content:
                    self.data[rule_num] = content
    
    def _format_data_for_save(self):
        """Format the rules data for saving to file."""
        lines = []
        for rule_num, content in sorted(self.data.items(), key=lambda x: self._rule_sorter(x[0])):
            lines.append(f"{rule_num}. {content}")
        return "\n".join(lines)
    
    def _rule_sorter(self, rule_key):
        """Sort rules numerically, handling complex rule numbers."""
        parts = rule_key.split('.')
        return [int(p) if p.isdigit() else p for p in parts]
    
    def _parse_rule_number(self, line):
        """Parse rule numbers including special formats."""
        # Match patterns like: "1.", "2.1.", "3.14159...", etc.
        pattern = r'^(\d+(?:\.\d+)?(?:\.\d+)*)'
        match = re.match(pattern, line)
        if match:
            return match.group(1).rstrip('.')
        return None

    def _get_rule_content(self, line):
        """Extract rule content after rule number."""
        # Find first occurrence of dot and space after numbers
        pattern = r'^[\d.]+\.\s*(.+)$'
        match = re.match(pattern, line)
        if match:
            return match.group(1).strip()
        return None
    
    def get_rule(self, rule_number):
        """Get rule by number, supports special rule numbers."""
        return self.get(str(rule_number))
    
    def search_rules(self, query):
        """Search rules by content."""
        return self.search(query)
