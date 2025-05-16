import discord
from discord.ext import commands
from discord import app_commands
from commands.ecomony.economy_manager import economy_manager
import random
import asyncio
from datetime import datetime, timedelta

class Beg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cooldowns = {}  # Store user cooldowns in memory
        
        # Responses for successful begging
        self.success_responses = [
            "Một người qua đường tặng bạn {amount} coin",
            "Ai đó thương hại bạn và cho {amount} coin",
            "Bạn tìm thấy {amount} coin dưới đất",
            "Một người giàu có cho bạn {amount} coin",
            "Một streamer nổi tiếng donate cho bạn {amount} coin",
            "Một người bạn cũ nhìn thấy bạn và cho {amount} coin"
        ]
        
        # Responses for failed begging
        self.fail_responses = [
            "Mọi người đều phớt lờ bạn",
            "Không ai quan tâm đến bạn cả",
            "Hôm nay không ai rảnh để cho bạn tiền",
            "Bạn nhìn không đủ đáng thương để xin tiền",
            "Mọi người đang vội, không ai dừng lại"
        ]

    @app_commands.command(name="beg", description="Xin tiền từ người qua đường")
    @app_commands.cooldown(1, 60, key=lambda i: i.user.id)  # 1 minute cooldown
    async def beg(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        
        try:
            user_id = interaction.user.id
            
            # Check if user is on cooldown
            if user_id in self.cooldowns:
                remaining = self.cooldowns[user_id] - datetime.now()
                if remaining.total_seconds() > 0:
                    minutes, seconds = divmod(int(remaining.total_seconds()), 60)
                    await interaction.followup.send(
                        f"❌ Bạn cần đợi thêm {minutes} phút {seconds} giây trước khi xin tiền lại.",
                        ephemeral=True
                    )
                    return
            
            # Check user data and last beg time
            user_data = economy_manager.get_user_data(user_id)
            
            # 70% chance of getting money
            if random.random() < 0.7:
                # Success, give money
                amount = random.randint(1, 20)
                new_balance = economy_manager.add_coins(user_id, amount)
                
                # Record the activity
                economy_manager.record_activity(user_id, "beg")
                
                # Select a random success message
                message = random.choice(self.success_responses).format(amount=amount)
                
                # Create embed
                embed = discord.Embed(
                    title="💸 Xin tiền thành công!",
                    description=message,
                    color=0x2ECC71  # Green color
                )
                embed.add_field(name="Số tiền nhận được", value=f"{amount:,} coin", inline=True)
                embed.add_field(name="Số dư hiện tại", value=f"{new_balance:,} coin", inline=True)
                embed.set_thumbnail(url=interaction.user.display_avatar.url)
                
                await interaction.followup.send(embed=embed)
            else:
                # Failed to get money
                message = random.choice(self.fail_responses)
                
                # Record the activity anyway
                economy_manager.record_activity(user_id, "beg")
                
                # Create embed
                embed = discord.Embed(
                    title="💔 Xin tiền thất bại!",
                    description=message,
                    color=0xE74C3C  # Red color
                )
                embed.set_thumbnail(url=interaction.user.display_avatar.url)
                
                await interaction.followup.send(embed=embed)
            
            # Set cooldown
            self.cooldowns[user_id] = datetime.now() + timedelta(minutes=1)
            
        except Exception as e:
            print(f"Error begging: {e}")
            await interaction.followup.send("❌ Đã xảy ra lỗi khi xin tiền. Vui lòng thử lại sau.")

async def setup(bot):
    await bot.add_cog(Beg(bot))
