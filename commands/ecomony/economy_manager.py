from database import MongoDatabase
from datetime import datetime

class EconomyManager:
    """Manages all economy-related operations using MongoDB."""
    
    def __init__(self):
        self.economy_db = MongoDatabase(collection_name="economy")
        self._ensure_connected()
        
    def _ensure_connected(self):
        """Ensure the database is connected."""
        if not self.economy_db.is_loaded:
            self.economy_db.load()
    
    def get_user_data(self, user_id):
        """Get a user's economic data from the database."""
        self._ensure_connected()
        
        # Try to get the user's data
        user_data = self.economy_db.get(str(user_id))
        
        if not user_data:
            # User doesn't exist, create a new entry with default values
            user_data = {
                "_id": str(user_id),
                "coin": 10,
                "bank": 0,
                "last_daily": None,
                "last_work": None, 
                "last_beg": None,
                "inventory": [],
                "job": None,
                "level": 1,
                "exp": 0
            }
            self.economy_db.set(str(user_id), user_data)
            
        return user_data
    
    def update_user_data(self, user_id, updates):
        """Update specific fields in a user's data."""
        self._ensure_connected()
        
        # Get current user data
        user_data = self.get_user_data(user_id)
        
        # Apply updates
        for key, value in updates.items():
            user_data[key] = value
        
        # Save the updated data
        self.economy_db.set(str(user_id), user_data)
        return user_data
    
    def add_coins(self, user_id, amount):
        """Add coins to a user's wallet."""
        self._ensure_connected()
        
        # Get current user data
        user_data = self.get_user_data(user_id)
        
        # Update balance
        current_balance = user_data.get("coin", 0)
        user_data["coin"] = current_balance + amount
        
        # Save the updated data
        self.economy_db.set(str(user_id), user_data)
        return user_data["coin"]
    
    def remove_coins(self, user_id, amount):
        """Remove coins from a user's wallet."""
        self._ensure_connected()
        
        # Get current user data
        user_data = self.get_user_data(user_id)
        
        # Check if user has enough coins
        current_balance = user_data.get("coin", 0)
        if current_balance < amount:
            return False, current_balance
        
        # Update balance
        user_data["coin"] = current_balance - amount
        
        # Save the updated data
        self.economy_db.set(str(user_id), user_data)
        return True, user_data["coin"]
    
    def deposit(self, user_id, amount):
        """Deposit coins from wallet to bank."""
        self._ensure_connected()
        
        # Get current user data
        user_data = self.get_user_data(user_id)
        
        # Check if user has enough coins in wallet
        current_wallet = user_data.get("coin", 0)
        if current_wallet < amount:
            return False, current_wallet, user_data.get("bank", 0)
        
        # Update balances
        user_data["coin"] = current_wallet - amount
        user_data["bank"] = user_data.get("bank", 0) + amount
        
        # Save the updated data
        self.economy_db.set(str(user_id), user_data)
        return True, user_data["coin"], user_data["bank"]
    
    def withdraw(self, user_id, amount):
        """Withdraw coins from bank to wallet."""
        self._ensure_connected()
        
        # Get current user data
        user_data = self.get_user_data(user_id)
        
        # Check if user has enough coins in bank
        current_bank = user_data.get("bank", 0)
        if current_bank < amount:
            return False, user_data.get("coin", 0), current_bank
        
        # Update balances
        user_data["bank"] = current_bank - amount
        user_data["coin"] = user_data.get("coin", 0) + amount
        
        # Save the updated data
        self.economy_db.set(str(user_id), user_data)
        return True, user_data["coin"], user_data["bank"]
    
    def record_activity(self, user_id, activity_type):
        """Record when a user performed a specific activity."""
        self._ensure_connected()
        
        # Get current user data
        user_data = self.get_user_data(user_id)
        
        # Update activity timestamp
        user_data[f"last_{activity_type}"] = datetime.now().isoformat()
        
        # Save the updated data
        self.economy_db.set(str(user_id), user_data)
        
    def transfer(self, from_user_id, to_user_id, amount):
        """Transfer coins from one user to another."""
        self._ensure_connected()
        
        # Get sender's data
        from_user_data = self.get_user_data(from_user_id)
        
        # Check if sender has enough coins
        sender_balance = from_user_data.get("coin", 0)
        if sender_balance < amount:
            return False, sender_balance
        
        # Remove coins from sender
        from_user_data["coin"] = sender_balance - amount
        self.economy_db.set(str(from_user_id), from_user_data)
        
        # Add coins to receiver
        receiver_balance = self.add_coins(to_user_id, amount)
        
        return True, from_user_data["coin"]

# Create a singleton instance
economy_manager = EconomyManager() 