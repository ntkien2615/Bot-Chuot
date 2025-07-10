import discord
from discord.ext import commands
from discord import app_commands


from commands.base_command import FunCommand


class Im(FunCommand):
    def __init__(self, bot):
        super().__init__(bot)

    @app_commands.command(name="im",description="im nao co be")
    @app_commands.describe(member="Nhập tên người bạn muốn bắt im")
    async def Im(self, interaction:discord.Interaction, member:discord.Member):
        if (member == None) or (member == interaction.user):
            await interaction.response.send_message('Nhập người nào vào đi',ephemeral=True)
            return
        else:
            embed = discord.Embed(title="", description="", color=discord.Color.random())
            embed.set_image(url="https://media.discordapp.net/attachments/883268139922636820/1125768473595875338/e6328ff4069e2184f8f212fd692ce117.png")
            await interaction.response.send_message(f"<@{member.id}> Im nào cô bé của tui", embed=embed)

async def setup(bot):
    await bot.add_cog(Im(bot))