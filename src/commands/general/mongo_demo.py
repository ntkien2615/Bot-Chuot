import discord
from discord import app_commands
from discord.ext import commands
from src.commands.base_command import GeneralCommand
from src.database import MongoDatabase

class MongoDemoCommand(GeneralCommand):
    """Commands to demonstrate MongoDB database usage."""
    
    def __init__(self, discord_bot):
        super().__init__(discord_bot)
        self.name = "mongodb"
        self.description = "MongoDB database demo commands"
        self.db = MongoDatabase(collection_name="demo_collection")
    
    async def _ensure_connection(self, interaction):
        """Helper to ensure database connection"""
        if not self.db.is_loaded and not self.db.load():
            await interaction.followup.send("❌ Không thể kết nối đến MongoDB.")
            return False
        return True
    
    @app_commands.command(name="save", description="Save data to MongoDB")
    @app_commands.describe(key="The key to store data under", value="The value to store")
    async def save_command(self, interaction: discord.Interaction, key: str, value: str):
        """Save a key-value pair to MongoDB."""
        await interaction.response.defer(ephemeral=False)
        
        if not await self._ensure_connection(interaction):
            return
        
        try:
            # Save the data
            self.db.set(key, value)
            await interaction.followup.send(f"✅ Đã lưu: {key} = {value}")
        except Exception as e:
            await interaction.followup.send(f"❌ Lỗi: {str(e)}")
    
    @app_commands.command(name="get", description="Get data from MongoDB")
    @app_commands.describe(key="The key to retrieve data for")
    async def get_command(self, interaction: discord.Interaction, key: str):
        """Retrieve a value by key from MongoDB."""
        await interaction.response.defer(ephemeral=False)
        
        if not await self._ensure_connection(interaction):
            return
        
        try:
            # Get the data
            result = self.db.get(key)
            
            if result:
                value = result.get("value", str({k: v for k, v in result.items() if k != "_id"}))
                await interaction.followup.send(f"🔍 '{key}': {value}")
            else:
                await interaction.followup.send(f"❌ Không tìm thấy '{key}'")
        except Exception as e:
            await interaction.followup.send(f"❌ Lỗi: {str(e)}")
    
    @app_commands.command(name="db_search", description="Search data in MongoDB")
    @app_commands.describe(query="The search term to look for")
    async def search_command(self, interaction: discord.Interaction, query: str):
        """Search for data in MongoDB."""
        await interaction.response.defer(ephemeral=False)
        
        if not await self._ensure_connection(interaction):
            return
        
        try:
            # Search for data
            results = self.db.search(query)
            
            if results:
                # Format results nicely
                formatted_results = [f"**{doc.pop('_id', 'unknown')}**: {doc}" for doc in results[:10]]
                result_text = "\n".join(formatted_results)
                if len(results) > 10:
                    result_text += f"\n... và {len(results) - 10} kết quả khác."
                await interaction.followup.send(f"🔍 Tìm thấy {len(results)} kết quả:\n{result_text}")
            else:
                await interaction.followup.send(f"❌ Không tìm thấy kết quả cho '{query}'")
        except Exception as e:
            await interaction.followup.send(f"❌ Lỗi: {str(e)}")
    
    @app_commands.command(name="delete", description="Delete data from MongoDB")
    @app_commands.describe(key="The key to delete data for")
    async def delete_command(self, interaction: discord.Interaction, key: str):
        """Delete data by key from MongoDB."""
        await interaction.response.defer(ephemeral=False)
        
        if not await self._ensure_connection(interaction):
            return
        
        try:
            # Delete the data
            result = self.db.delete(key)
            
            if result.deleted_count > 0:
                await interaction.followup.send(f"✅ Đã xóa '{key}'")
            else:
                await interaction.followup.send(f"❌ Không tìm thấy '{key}'")
        except Exception as e:
            await interaction.followup.send(f"❌ Lỗi: {str(e)}")
    
    @app_commands.command(name="test", description="Test MongoDB connection")
    async def test_command(self, interaction: discord.Interaction):
        """Test the connection to MongoDB."""
        await interaction.response.defer(ephemeral=False)
        
        try:
            # Reset the connection
            if self.db.is_loaded:
                self.db.close()
            
            # Try to connect
            if self.db.load():
                await interaction.followup.send("✅ Kết nối MongoDB thành công!")
            else:
                await interaction.followup.send("❌ Không thể kết nối MongoDB.")
        except Exception as e:
            await interaction.followup.send(f"❌ Lỗi: {str(e)}")