import discord
from discord import app_commands
from discord.ext import commands
from commands.base_command import GeneralCommand
from database import MongoDatabase
from config import Config

class MongoDemoCommand(GeneralCommand):
    """Commands to demonstrate MongoDB database usage."""
    
    def __init__(self, bot):
        super().__init__(bot)
        self.name = "mongodb"
        self.description = "MongoDB database demo commands"
        self.db = MongoDatabase(collection_name="demo_collection")
    
    @app_commands.command(name="save", description="Save data to MongoDB")
    @app_commands.describe(key="The key to store data under", value="The value to store")
    async def save_command(self, interaction: discord.Interaction, key: str, value: str):
        """Save a key-value pair to MongoDB."""
        await interaction.response.defer(ephemeral=False)
        
        # Make sure the database is connected
        if not self.db.is_loaded:
            if not self.db.load():
                await interaction.followup.send("❌ Không thể kết nối đến MongoDB. Vui lòng kiểm tra cấu hình.")
                return
        
        try:
            # Save the data
            self.db.set(key, value)
            await interaction.followup.send(f"✅ Đã lưu: {key} = {value}")
        except Exception as e:
            await interaction.followup.send(f"❌ Lỗi khi lưu dữ liệu: {str(e)}")
    
    @app_commands.command(name="get", description="Get data from MongoDB")
    @app_commands.describe(key="The key to retrieve data for")
    async def get_command(self, interaction: discord.Interaction, key: str):
        """Retrieve a value by key from MongoDB."""
        await interaction.response.defer(ephemeral=False)
        
        # Make sure the database is connected
        if not self.db.is_loaded:
            if not self.db.load():
                await interaction.followup.send("❌ Không thể kết nối đến MongoDB. Vui lòng kiểm tra cấu hình.")
                return
        
        try:
            # Get the data
            result = self.db.get(key)
            
            if result:
                if "value" in result:
                    value = result["value"]
                else:
                    # Remove _id from the result for cleaner display
                    if "_id" in result:
                        del result["_id"]
                    value = str(result)
                
                await interaction.followup.send(f"🔍 Tìm thấy dữ liệu cho '{key}': {value}")
            else:
                await interaction.followup.send(f"❌ Không tìm thấy dữ liệu cho '{key}'")
        except Exception as e:
            await interaction.followup.send(f"❌ Lỗi khi lấy dữ liệu: {str(e)}")
    
    @app_commands.command(name="search", description="Search data in MongoDB")
    @app_commands.describe(query="The search term to look for")
    async def search_command(self, interaction: discord.Interaction, query: str):
        """Search for data in MongoDB."""
        await interaction.response.defer(ephemeral=False)
        
        # Make sure the database is connected
        if not self.db.is_loaded:
            if not self.db.load():
                await interaction.followup.send("❌ Không thể kết nối đến MongoDB. Vui lòng kiểm tra cấu hình.")
                return
        
        try:
            # Search for data
            results = self.db.search(query)
            
            if results:
                # Format results nicely
                formatted_results = []
                for doc in results:
                    # Remove _id from the display
                    doc_id = doc.pop("_id", "unknown")
                    formatted_results.append(f"**{doc_id}**: {doc}")
                
                # Join results with newlines
                result_text = "\n".join(formatted_results[:10])  # Limit to 10 results
                
                if len(results) > 10:
                    result_text += f"\n... và {len(results) - 10} kết quả khác."
                
                await interaction.followup.send(f"🔍 Tìm thấy {len(results)} kết quả cho '{query}':\n{result_text}")
            else:
                await interaction.followup.send(f"❌ Không tìm thấy kết quả cho '{query}'")
        except Exception as e:
            await interaction.followup.send(f"❌ Lỗi khi tìm kiếm dữ liệu: {str(e)}")
    
    @app_commands.command(name="delete", description="Delete data from MongoDB")
    @app_commands.describe(key="The key to delete data for")
    async def delete_command(self, interaction: discord.Interaction, key: str):
        """Delete data by key from MongoDB."""
        await interaction.response.defer(ephemeral=False)
        
        # Make sure the database is connected
        if not self.db.is_loaded:
            if not self.db.load():
                await interaction.followup.send("❌ Không thể kết nối đến MongoDB. Vui lòng kiểm tra cấu hình.")
                return
        
        try:
            # Delete the data
            result = self.db.delete(key)
            
            if result.deleted_count > 0:
                await interaction.followup.send(f"✅ Đã xóa dữ liệu cho '{key}'")
            else:
                await interaction.followup.send(f"❌ Không tìm thấy dữ liệu cho '{key}'")
        except Exception as e:
            await interaction.followup.send(f"❌ Lỗi khi xóa dữ liệu: {str(e)}")
    
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
                await interaction.followup.send("✅ Kết nối đến MongoDB thành công!")
            else:
                await interaction.followup.send("❌ Không thể kết nối đến MongoDB. Vui lòng kiểm tra cấu hình.")
        except Exception as e:
            await interaction.followup.send(f"❌ Lỗi khi kết nối đến MongoDB: {str(e)}")

async def setup(bot):
    """Set up the Cog for the bot."""
    await bot.add_cog(MongoDemoCommand(bot)) 