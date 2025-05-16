import discord
from discord.ext import commands
from discord import app_commands
from commands.ecomony.economy_manager import economy_manager

class Balance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="balance", description="Kiểm tra số dư tài khoản của bạn")
    async def balance(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        
        try:
            user_id = interaction.user.id
            user_data = economy_manager.get_user_data(user_id)
            
            wallet = user_data.get("coin", 0)
            bank = user_data.get("bank", 0)
            total = wallet + bank
            
            # Create a nice embed for the balance
            embed = discord.Embed(
                title="💰 Số dư tài khoản",
                description=f"**{interaction.user.display_name}**",
                color=0xF1C40F  # Gold color
            )
            embed.add_field(name="💵 Ví tiền", value=f"{wallet:,} coin", inline=True)
            embed.add_field(name="🏦 Ngân hàng", value=f"{bank:,} coin", inline=True)
            embed.add_field(name="💸 Tổng cộng", value=f"{total:,} coin", inline=False)
            embed.set_thumbnail(url=interaction.user.display_avatar.url)
            
            await interaction.followup.send(embed=embed)
            
        except Exception as e:
            print(f"Error checking balance: {e}")
            await interaction.followup.send("❌ Đã xảy ra lỗi khi kiểm tra số dư. Vui lòng thử lại sau.")

    @app_commands.command(name="deposit", description="Gửi tiền vào ngân hàng")
    @app_commands.describe(amount="Số tiền muốn gửi vào ngân hàng")
    async def deposit(self, interaction: discord.Interaction, amount: int):
        await interaction.response.defer(ephemeral=False)
        
        try:
            if amount <= 0:
                await interaction.followup.send("❌ Số tiền phải lớn hơn 0.")
                return
                
            user_id = interaction.user.id
            success, wallet, bank = economy_manager.deposit(user_id, amount)
            
            if success:
                embed = discord.Embed(
                    title="🏦 Gửi tiền thành công",
                    description=f"**{interaction.user.display_name}** đã gửi **{amount:,}** coin vào ngân hàng.",
                    color=0x2ECC71  # Green color
                )
                embed.add_field(name="💵 Ví tiền", value=f"{wallet:,} coin", inline=True)
                embed.add_field(name="🏦 Ngân hàng", value=f"{bank:,} coin", inline=True)
                embed.set_thumbnail(url=interaction.user.display_avatar.url)
                
                await interaction.followup.send(embed=embed)
            else:
                await interaction.followup.send(
                    f"❌ Bạn không có đủ tiền để gửi. Số dư hiện tại: {wallet:,} coin."
                )
                
        except Exception as e:
            print(f"Error depositing: {e}")
            await interaction.followup.send("❌ Đã xảy ra lỗi khi gửi tiền. Vui lòng thử lại sau.")
            
    @app_commands.command(name="withdraw", description="Rút tiền từ ngân hàng")
    @app_commands.describe(amount="Số tiền muốn rút từ ngân hàng")
    async def withdraw(self, interaction: discord.Interaction, amount: int):
        await interaction.response.defer(ephemeral=False)
        
        try:
            if amount <= 0:
                await interaction.followup.send("❌ Số tiền phải lớn hơn 0.")
                return
                
            user_id = interaction.user.id
            success, wallet, bank = economy_manager.withdraw(user_id, amount)
            
            if success:
                embed = discord.Embed(
                    title="💰 Rút tiền thành công",
                    description=f"**{interaction.user.display_name}** đã rút **{amount:,}** coin từ ngân hàng.",
                    color=0x2ECC71  # Green color
                )
                embed.add_field(name="💵 Ví tiền", value=f"{wallet:,} coin", inline=True)
                embed.add_field(name="🏦 Ngân hàng", value=f"{bank:,} coin", inline=True)
                embed.set_thumbnail(url=interaction.user.display_avatar.url)
                
                await interaction.followup.send(embed=embed)
            else:
                await interaction.followup.send(
                    f"❌ Bạn không có đủ tiền trong ngân hàng để rút. Số dư ngân hàng: {bank:,} coin."
                )
                
        except Exception as e:
            print(f"Error withdrawing: {e}")
            await interaction.followup.send("❌ Đã xảy ra lỗi khi rút tiền. Vui lòng thử lại sau.")

async def setup(bot):
    await bot.add_cog(Balance(bot))