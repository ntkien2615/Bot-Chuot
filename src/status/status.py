import discord
from discord.ext import commands


class CommandSyncer(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    try:
      guild = discord.Object(id=1077151200182542347)
      synced = await self.bot.tree.sync(guild=guild)
      print(f'Synced {len(synced)} commands to test guild 1077151200182542347')
    except Exception as e:
      print(f'Lỗi: {e}')
         
async def setup(bot):
  await bot.add_cog(CommandSyncer(bot))