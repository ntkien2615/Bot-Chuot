"""
Database managers for different collections in MongoDB.
"""
from database import MongoDatabase
from datetime import datetime
import json


class UserProfileManager:
    """Manages user profiles collection."""
    
    def __init__(self):
        self.db = MongoDatabase(collection_name="user_profiles")
        self._ensure_connected()
    
    def _ensure_connected(self):
        """Ensure the database is connected."""
        if not self.db.is_loaded:
            self.db.load()
    
    def get_user_profile(self, user_id):
        """Get user profile data."""
        self._ensure_connected()
        
        profile = self.db.get(str(user_id))
        if not profile:
            # Create default profile
            profile = {
                "_id": str(user_id),
                "username": None,
                "display_name": None,
                "joined_at": datetime.now().isoformat(),
                "avatar_url": None,
                "preferences": {
                    "language": "vi",
                    "notifications": True,
                    "privacy": "public"
                },
                "stats": {
                    "commands_used": 0,
                    "games_played": 0,
                    "messages_sent": 0
                }
            }
            self.db.set(str(user_id), profile)
        
        return profile
    
    def update_profile(self, user_id, updates):
        """Update user profile."""
        self._ensure_connected()
        profile = self.get_user_profile(user_id)
        
        # Apply updates
        for key, value in updates.items():
            if key in ["preferences", "stats"] and isinstance(value, dict):
                profile[key].update(value)
            else:
                profile[key] = value
        
        self.db.set(str(user_id), profile)
        return profile
    
    def increment_command_usage(self, user_id):
        """Increment command usage count."""
        profile = self.get_user_profile(user_id)
        profile["stats"]["commands_used"] += 1
        self.db.set(str(user_id), profile)
    
    def increment_games_played(self, user_id):
        """Increment games played count."""
        profile = self.get_user_profile(user_id)
        profile["stats"]["games_played"] += 1
        self.db.set(str(user_id), profile)


class GameStatsManager:
    """Manages game statistics collection."""
    
    def __init__(self):
        self.db = MongoDatabase(collection_name="game_stats")
        self._ensure_connected()
    
    def _ensure_connected(self):
        """Ensure the database is connected."""
        if not self.db.is_loaded:
            self.db.load()
    
    def get_game_stats(self, user_id):
        """Get user game statistics."""
        self._ensure_connected()
        
        stats = self.db.get(str(user_id))
        if not stats:
            # Create default stats
            stats = {
                "_id": str(user_id),
                "rps": {"wins": 0, "losses": 0, "draws": 0},
                "dice": {"total_rolls": 0, "highest_roll": 0},
                "poker": {"games_played": 0, "best_hand": None},
                "guess_number": {"attempts": 0, "correct_guesses": 0},
                "tai_xiu": {"wins": 0, "losses": 0, "coins_won": 0, "coins_lost": 0}
            }
            self.db.set(str(user_id), stats)
        
        return stats
    
    def update_rps_stats(self, user_id, result):
        """Update Rock Paper Scissors stats."""
        stats = self.get_game_stats(user_id)
        stats["rps"][result] += 1
        self.db.set(str(user_id), stats)
    
    def update_dice_stats(self, user_id, roll_value):
        """Update dice roll stats."""
        stats = self.get_game_stats(user_id)
        stats["dice"]["total_rolls"] += 1
        if roll_value > stats["dice"]["highest_roll"]:
            stats["dice"]["highest_roll"] = roll_value
        self.db.set(str(user_id), stats)
    
    def update_tai_xiu_stats(self, user_id, won, coins_amount):
        """Update Tai Xiu game stats."""
        stats = self.get_game_stats(user_id)
        if won:
            stats["tai_xiu"]["wins"] += 1
            stats["tai_xiu"]["coins_won"] += coins_amount
        else:
            stats["tai_xiu"]["losses"] += 1
            stats["tai_xiu"]["coins_lost"] += coins_amount
        self.db.set(str(user_id), stats)


class ServerSettingsManager:
    """Manages server settings collection."""
    
    def __init__(self):
        self.db = MongoDatabase(collection_name="server_settings")
        self._ensure_connected()
    
    def _ensure_connected(self):
        """Ensure the database is connected."""
        if not self.db.is_loaded:
            self.db.load()
    
    def get_server_settings(self, guild_id):
        """Get server settings."""
        self._ensure_connected()
        
        settings = self.db.get(str(guild_id))
        if not settings:
            # Create default settings
            settings = {
                "_id": str(guild_id),
                "prefix": "!",
                "welcome_channel": None,
                "log_channel": None,
                "economy_enabled": True,
                "fun_commands_enabled": True,
                "moderation": {
                    "auto_mod": False,
                    "spam_protection": True
                },
                "custom_commands": []
            }
            self.db.set(str(guild_id), settings)
        
        return settings
    
    def update_settings(self, guild_id, updates):
        """Update server settings."""
        settings = self.get_server_settings(guild_id)
        
        for key, value in updates.items():
            if key == "moderation" and isinstance(value, dict):
                settings["moderation"].update(value)
            else:
                settings[key] = value
        
        self.db.set(str(guild_id), settings)
        return settings


class TransactionManager:
    """Manages transaction history collection."""
    
    def __init__(self):
        self.db = MongoDatabase(collection_name="transactions")
        self._ensure_connected()
        self.transaction_counter = 0
    
    def _ensure_connected(self):
        """Ensure the database is connected."""
        if not self.db.is_loaded:
            self.db.load()
    
    def record_transaction(self, from_user, to_user, amount, transaction_type, description=""):
        """Record a transaction."""
        self._ensure_connected()
        
        # Generate unique transaction ID
        transaction_id = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{self.transaction_counter}"
        self.transaction_counter += 1
        
        transaction = {
            "_id": transaction_id,
            "from_user": str(from_user) if from_user else None,
            "to_user": str(to_user) if to_user else None,
            "amount": amount,
            "type": transaction_type,  # transfer, beg, work, daily, game_win, game_loss
            "timestamp": datetime.now().isoformat(),
            "description": description
        }
        
        self.db.set(transaction_id, transaction)
        return transaction_id
    
    def get_user_transactions(self, user_id, limit=10):
        """Get recent transactions for a user."""
        self._ensure_connected()
        
        # Find transactions where user is involved
        query = {
            "$or": [
                {"from_user": str(user_id)},
                {"to_user": str(user_id)}
            ]
        }
        
        transactions = self.db.find(query)
        # Sort by timestamp (most recent first)
        transactions.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        
        return transactions[:limit]


# Create singleton instances
user_profile_manager = UserProfileManager()
game_stats_manager = GameStatsManager()
server_settings_manager = ServerSettingsManager()
transaction_manager = TransactionManager()
