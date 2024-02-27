import discord
import pyjokes
from discord.ext import commands


class joke(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def joke(self, ctx):
        msg = discord.Embed(title="Coder Joke v1.ABC",
                            color=discord.Colour.random())
        msg.add_field(name="",
                      value=pyjokes.get_joke(
                          language='en', category='neutral'),
                      inline=False)
        await ctx.send(embed=msg)


async def setup(bot):
    await bot.add_cog(joke(bot))
