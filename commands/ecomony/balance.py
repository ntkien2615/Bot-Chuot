import discord
from discord.ext import commands
from discord import app_commands
from commands.ecomony.economy_manager import economy_manager

class Balance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def _create_balance_embed(self, user, wallet, bank, title="💰 Số dư tài khoản"):
        """Helper method to create balance embed"""
        embed = discord.Embed(title=title, description=f"**{user.display_name}**", color=0xF1C40F)
        embed.add_field(name="💵 Ví tiền", value=f"{wallet:,} coin", inline=True)
        embed.add_field(name="🏦 Ngân hàng", value=f"{bank:,} coin", inline=True)
        if title == "💰 Số dư tài khoản":
            embed.add_field(name="💸 Tổng cộng", value=f"{wallet + bank:,} coin", inline=False)
        embed.set_thumbnail(url=user.display_avatar.url)
        return embed

    @app_commands.command(name="balance", description="Kiểm tra số dư tài khoản của bạn")
    async def balance(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        
        try:
            user_data = economy_manager.get_user_data(interaction.user.id)
            wallet = user_data.get("coin", 0)
            bank = user_data.get("bank", 0)
            
            embed = self._create_balance_embed(interaction.user, wallet, bank)
            await interaction.followup.send(embed=embed)
            
        except Exception as e:
            print(f"Error checking balance: {e}")
            await interaction.followup.send("❌ Đã xảy ra lỗi. Vui lòng thử lại sau.")

    @app_commands.command(name="deposit", description="Gửi tiền vào ngân hàng")
    @app_commands.describe(amount="Số tiền muốn gửi vào ngân hàng")
    async def deposit(self, interaction: discord.Interaction, amount: int):
        await interaction.response.defer(ephemeral=False)
        
        if amount <= 0:
            await interaction.followup.send("❌ Số tiền phải lớn hơn 0.")
            return
            
        try:
            success, wallet, bank = economy_manager.deposit(interaction.user.id, amount)
            
            if success:
                embed = self._create_balance_embed(interaction.user, wallet, bank, "🏦 Gửi tiền thành công")
                embed.description = f"**{interaction.user.display_name}** đã gửi **{amount:,}** coin vào ngân hàng."
                embed.color = 0x2ECC71
                await interaction.followup.send(embed=embed)
            else:
                await interaction.followup.send(f"❌ Bạn không có đủ tiền để gửi. Số dư hiện tại: {wallet:,} coin.")
                
        except Exception as e:
            print(f"Error depositing: {e}")
            await interaction.followup.send("❌ Đã xảy ra lỗi. Vui lòng thử lại sau.")
            
    @app_commands.command(name="withdraw", description="Rút tiền từ ngân hàng")
    @app_commands.describe(amount="Số tiền muốn rút từ ngân hàng")
    async def withdraw(self, interaction: discord.Interaction, amount: int):
        await interaction.response.defer(ephemeral=False)
        
        if amount <= 0:
            await interaction.followup.send("❌ Số tiền phải lớn hơn 0.")
            return
            
        try:
            success, wallet, bank = economy_manager.withdraw(interaction.user.id, amount)
            
            if success:
                embed = self._create_balance_embed(interaction.user, wallet, bank, "💰 Rút tiền thành công")
                embed.description = f"**{interaction.user.display_name}** đã rút **{amount:,}** coin từ ngân hàng."
                embed.color = 0x2ECC71
                await interaction.followup.send(embed=embed)
            else:
                await interaction.followup.send(f"❌ Số dư ngân hàng không đủ: {bank:,} coin.")
                
        except Exception as e:
            print(f"Error withdrawing: {e}")
            await interaction.followup.send("❌ Đã xảy ra lỗi. Vui lòng thử lại sau.")

async def setup(bot):
    await bot.add_cog(Balance(bot))