import discord, aiosqlite
from discord.ext import commands


class rd(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  # @commands.Cog.listener()
  # async def on_ready(self):
  #   db = aiosqlite.connect("./db/main.sqlite")
  #   cursor = db.cursor()
  #   cursor.execute('CREATE TABLE IF NOT EXISTS main(user_id INTEGER, wallet INTEGER, bank INTEGER)')

  # @commands.Cog.listener()
  # async def on_message(self, message):
  #   if message.author.bot:
  #     return
  
  #   author = message.author
  #   db = aiosqlite.connect('./db/main.main.sqlite')
  #   cursor = db.cursor()
  #   cursor.execute(f'SELECT user_id FROM main WHERE user_id ={author.id}')
  #   result = cursor.fetchone()
    
  #   if result is None:
  #     sql = ('INSERT INTO main(user_id, wallet, bank) VALUES (?,?,?)')
  #     val = (author.id,0,0)
  #     cursor.execute(sql,val)

  #   db.comit()
  #   cursor.close()
  #   db.close()

  @commands.Cog.listener()
  async def on_ready(self):
    try:
      synced = await self.bot.tree.sync()
      print(f'{len(synced)}')
    except Exception as e:
      print(f'Lỗi: {e}')

async def setup(bot):
  await bot.add_cog(rd(bot))