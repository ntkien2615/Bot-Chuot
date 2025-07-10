import discord
from discord.ext import commands
from discord import app_commands
import pyjokes


from commands.base_command import FunCommand


class codejoke(FunCommand):
    def __init__(self, bot):
        super().__init__(bot)

    @app_commands.command(name='codejoke',description='Tạo code joke (chỉ hỗ trợ tiếng anh)') 
    async def codejoke_command(self, interaction:discord.Interaction):
        msg = discord.Embed(title="Coder Joke v1.ABC",
                            color=discord.Colour.random())
        msg.add_field(name="",
                      value=pyjokes.get_joke(
                          language='en', category='neutral'),
                      inline=False)
        await interaction.response.send_message(embed=msg)
        
async def setup(bot):
    await bot.add_cog(codejoke(bot))