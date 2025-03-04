import discord
from discord.ext import commands
from discord import app_commands


class hug(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @app_commands.command(name='hug', description='Ôm homie của bạn')
    @app_commands.describe(user='Người bạn muốn ôm')
    async def hug(self, interaction: discord.Interaction, user:discord.Member):
        if user == None:
            interaction.user = user
        embed = discord.Embed(title="", description=f'{interaction.user} đã ôm {user.mention}, thật ngọt ngào!!!', color=discord.Color.random())
        embed.set_image(url="https://media.discordapp.net/attachments/1077255654512787537/1346371351128051712/images.png?ex=67c7f188&is=67c6a008&hm=89e6adae2479be8138071a3a6fdf9c312daeb6297e5062c9c3a03830782d3135&=&format=webp&quality=lossless&width=376&height=210")
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(hug(bot))