import discord, aiosqlite
from discord.ext import commands


class rd(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    try:
      synced = await self.bot.tree.sync()
      print(f'{len(synced)}')
    except Exception as e:
      print(f'Lỗi: {e}')
         
async def setup(bot):
  await bot.add_cog(rd(bot))