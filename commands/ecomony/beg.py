import discord
from discord.ext import commands
from discord import app_commands
from commands.ecomony.economy_manager import economy_manager
import random
from datetime import datetime, timedelta

class Beg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        # Simplified responses
        self.success_responses = [
            "Một người qua đường tặng bạn {amount} coin",
            "Bạn tìm thấy {amount} coin dưới đất",
            "Một người giàu có cho bạn {amount} coin",
            "Một streamer nổi tiếng donate cho bạn {amount} coin"
        ]
        
        self.fail_responses = [
            "Mọi người đều phớt lờ bạn",
            "Không ai quan tâm đến bạn cả",
            "Hôm nay không ai rảnh để cho bạn tiền"
        ]

    @app_commands.command(name="beg", description="Xin tiền từ người qua đường")
    @app_commands.cooldown(1, 60, key=lambda i: i.user.id)
    async def beg(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        
        try:
            user_id = interaction.user.id
            
            # 70% chance of getting money
            if random.random() < 0.7:
                amount = random.randint(1, 20)
                new_balance = economy_manager.add_coins(user_id, amount)
                economy_manager.record_activity(user_id, "beg")
                
                message = random.choice(self.success_responses).format(amount=amount)
                embed = discord.Embed(
                    title="💸 Xin tiền thành công!",
                    description=message,
                    color=0x2ECC71
                )
                embed.add_field(name="Số tiền nhận được", value=f"{amount:,} coin", inline=True)
                embed.add_field(name="Số dư hiện tại", value=f"{new_balance:,} coin", inline=True)
            else:
                economy_manager.record_activity(user_id, "beg")
                message = random.choice(self.fail_responses)
                embed = discord.Embed(
                    title="💔 Xin tiền thất bại!",
                    description=message,
                    color=0xE74C3C
                )
            
            embed.set_thumbnail(url=interaction.user.display_avatar.url)
            await interaction.followup.send(embed=embed)
            
        except Exception as e:
            print(f"Error begging: {e}")
            await interaction.followup.send("❌ Đã xảy ra lỗi khi xin tiền. Vui lòng thử lại sau.")

async def setup(bot):
    await bot.add_cog(Beg(bot))
