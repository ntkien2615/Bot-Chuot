import discord
from discord.ext import commands
from discord import app_commands


class legslash(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='mp5_leg', description='cẩn thận cặp giò của m đấy')
    @app_commands.describe(member='Chọn cái đứa nào ây')
    async def leg(self, interaction: discord.Interaction, member: discord.Member = None):
        if member == None:
            await interaction.response.send_message('Well, ko có ai làm sao có cặp giò', ephemeral=True)
            return
        elif member == interaction.user:
            await interaction.response.send_message(f"Thiệt luôn, mà cặp giò của bạn trông khá múp ấy {member}")
        else:
            embed = discord.Embed(title="", description=f"", color=discord.Color.random())
            embed.set_image(url="https://media.discordapp.net/attachments/1077151202040614988/1266412244976140328/yukka.jpg?ex=66a50dd0&is=66a3bc50&hm=62543a0caa799b92258c2641f7b8633fa0a8d6e8bd1bc7c4c460a51cd9aabb83&=&format=webp&width=418&height=350")
            await interaction.response.send_message(f"<@{member.id}> CAN THAN CAI CAP GIO VOI HAI DON M DAY",embed=embed)

async def setup(bot):
    await bot.add_cog(legslash(bot))