import os
import json
from dotenv import load_dotenv, find_dotenv

class Config:
    """Configuration manager for the bot."""
    
    _instance = None
    
    def __new__(cls):
        """Implement the Singleton pattern."""
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize the config manager (only once due to Singleton pattern)."""
        if self._initialized:
            return
        
        self._initialized = True
        self.load_env_vars()
        self.bot_config = {}
        self.load_config()
    
    def load_env_vars(self):
        """Load environment variables."""
        # Check for .env in Render's secret file location first
        render_env_path = "/etc/secrets/.env"
        if os.path.exists(render_env_path):
            load_dotenv(dotenv_path=render_env_path)
        else:
            # Fallback for local development
            load_dotenv(find_dotenv())
        self.discord_token = os.getenv("discord_token")
        self.bot_owner_id = os.getenv("bot_owner_id")
        self.debug_mode = os.getenv("debug_mode", "False").lower() == "true"
        self.test_guild_id = os.getenv("test_guild_id")
        
        # MongoDB configuration
        self.mongodb_uri = os.getenv("MONGODB_URI")
        self.mongodb_database = os.getenv("MONGODB_DATABASE", "botchuot")
    
    def load_config(self):
        """Load configuration from config.json if exists."""
        config_path = "config.json"
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    self.bot_config = json.load(f)
            except Exception as e:
                print(f"Error loading config: {e}")
                self.bot_config = {}
    
    def save_config(self):
        """Save configuration to config.json."""
        config_path = "config.json"
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(self.bot_config, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def get(self, key, default=None):
        """Get a configuration value."""
        return self.bot_config.get(key, default)
    
    def set(self, key, value):
        """Set a configuration value."""
        self.bot_config[key] = value
        return self.save_config()
    
    def get_token(self):
        """Get the Discord token."""
        return self.discord_token
    
    def get_owner_id(self):
        """Get the bot owner ID."""
        return self.bot_owner_id
    
    def is_debug_mode(self):
        """Check if debug mode is enabled."""
        return self.debug_mode
    
    def get_mongodb_uri(self):
        """Get the MongoDB URI."""
        return self.mongodb_uri
    
    def get_mongodb_database(self):
        """Get the MongoDB database name."""
        return self.mongodb_database
        
    def get_test_guild_id(self):
        """Get the test guild ID for guild-specific command syncing."""
        return self.test_guild_id 