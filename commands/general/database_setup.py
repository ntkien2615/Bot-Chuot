import discord
from discord.ext import commands
from discord import app_commands
from database_managers import (
    user_profile_manager, 
    game_stats_manager, 
    server_settings_manager, 
    transaction_manager
)
from commands.ecomony.economy_manager import economy_manager
import random


class DatabaseSetup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="setup_database", description="Tạo và thiết lập tất cả collections trong MongoDB")
    async def setup_database(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        
        try:
            user_id = interaction.user.id
            guild_id = interaction.guild.id if interaction.guild else None
            
            embed = discord.Embed(
                title="🗄️ Thiết lập Database",
                description="Đang tạo và thiết lập các collections...",
                color=0x3498DB
            )
            
            # Test economy collection
            economy_data = economy_manager.get_user_data(user_id)
            embed.add_field(
                name="💰 Economy Collection", 
                value=f"✅ Đã tạo với {economy_data.get('coin', 0)} coins", 
                inline=False
            )
            
            # Test user profiles collection
            profile_data = user_profile_manager.get_user_profile(user_id)
            user_profile_manager.update_profile(user_id, {
                "username": interaction.user.name,
                "display_name": interaction.user.display_name,
                "avatar_url": str(interaction.user.display_avatar.url)
            })
            embed.add_field(
                name="👤 User Profiles Collection", 
                value=f"✅ Đã tạo profile cho {interaction.user.display_name}", 
                inline=False
            )
            
            # Test game stats collection
            game_stats = game_stats_manager.get_game_stats(user_id)
            # Add some sample stats
            game_stats_manager.update_rps_stats(user_id, "wins")
            game_stats_manager.update_dice_stats(user_id, random.randint(1, 6))
            embed.add_field(
                name="🎮 Game Stats Collection", 
                value="✅ Đã tạo và thêm thống kê game mẫu", 
                inline=False
            )
            
            # Test server settings collection (only if in a guild)
            if guild_id:
                server_settings = server_settings_manager.get_server_settings(guild_id)
                embed.add_field(
                    name="⚙️ Server Settings Collection", 
                    value=f"✅ Đã tạo cài đặt cho server {interaction.guild.name}", 
                    inline=False
                )
            
            # Test transactions collection
            transaction_id = transaction_manager.record_transaction(
                from_user=None,
                to_user=user_id,
                amount=100,
                transaction_type="setup_bonus",
                description="Database setup bonus"
            )
            embed.add_field(
                name="📋 Transactions Collection", 
                value=f"✅ Đã tạo và ghi transaction #{transaction_id}", 
                inline=False
            )
            
            # Add bonus coins for testing
            economy_manager.add_coins(user_id, 100)
            
            embed.add_field(
                name="🎁 Phần thưởng", 
                value="Bạn đã nhận 100 coins cho việc thiết lập database!", 
                inline=False
            )
            
            embed.set_footer(text="Tất cả collections đã được tạo thành công!")
            embed.set_thumbnail(url=interaction.user.display_avatar.url)
            
            await interaction.followup.send(embed=embed)
            
        except Exception as e:
            print(f"Error setting up database: {e}")
            await interaction.followup.send("❌ Đã xảy ra lỗi khi thiết lập database.")

    @app_commands.command(name="check_collections", description="Kiểm tra tất cả collections trong MongoDB")
    async def check_collections(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        
        try:
            user_id = interaction.user.id
            
            embed = discord.Embed(
                title="📊 Trạng thái Collections",
                description="Kiểm tra dữ liệu trong các collections...",
                color=0x2ECC71
            )
            
            # Check economy data
            economy_data = economy_manager.get_user_data(user_id)
            embed.add_field(
                name="💰 Economy", 
                value=f"Coins: {economy_data.get('coin', 0):,}\nBank: {economy_data.get('bank', 0):,}\nLevel: {economy_data.get('level', 1)}", 
                inline=True
            )
            
            # Check profile data
            profile_data = user_profile_manager.get_user_profile(user_id)
            commands_used = profile_data.get('stats', {}).get('commands_used', 0)
            games_played = profile_data.get('stats', {}).get('games_played', 0)
            embed.add_field(
                name="👤 Profile", 
                value=f"Commands: {commands_used}\nGames: {games_played}\nJoined: {profile_data.get('joined_at', 'N/A')[:10]}", 
                inline=True
            )
            
            # Check game stats
            game_stats = game_stats_manager.get_game_stats(user_id)
            rps_wins = game_stats.get('rps', {}).get('wins', 0)
            dice_rolls = game_stats.get('dice', {}).get('total_rolls', 0)
            embed.add_field(
                name="🎮 Game Stats", 
                value=f"RPS Wins: {rps_wins}\nDice Rolls: {dice_rolls}\nTai Xiu W/L: {game_stats.get('tai_xiu', {}).get('wins', 0)}/{game_stats.get('tai_xiu', {}).get('losses', 0)}", 
                inline=True
            )
            
            # Check recent transactions
            transactions = transaction_manager.get_user_transactions(user_id, limit=3)
            transaction_info = f"Total: {len(transactions)} transactions"
            if transactions:
                latest = transactions[0]
                transaction_info += f"\nLatest: {latest.get('type', 'N/A')} ({latest.get('amount', 0)} coins)"
            
            embed.add_field(
                name="📋 Transactions", 
                value=transaction_info, 
                inline=True
            )
            
            embed.set_thumbnail(url=interaction.user.display_avatar.url)
            embed.set_footer(text="Dữ liệu từ MongoDB Atlas")
            
            await interaction.followup.send(embed=embed)
            
        except Exception as e:
            print(f"Error checking collections: {e}")
            await interaction.followup.send("❌ Đã xảy ra lỗi khi kiểm tra collections.")


async def setup(bot):
    await bot.add_cog(DatabaseSetup(bot))
