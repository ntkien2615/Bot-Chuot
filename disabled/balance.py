import discord,aiosqlite
from discord import app_commands
from discord.ext import commands


class balance(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @app_commands.command(name="balance",description="xem thử ví bạn (người khác) còn bao nhiêu")
    async def balance(self, interaction:discord.Interaction,member: discord.Member = None):
        if member == None:
            member = interaction.user

        db = aiosqlite.connect("./db/eco.sqlite")
        cursor = db.cursor()

        
        cursor.execute(f'SELECT wallet,bank FROM eco WHERE user_id = {author.id}')
        bal = cursor.fetchone()

        try:
            wallet = bal[0]
            bank = bal[1]
        except:
            wallet = 0
            bank   = 1

        await interaction.response.send_message(f'{wallet} -- {bank}')
        
        
        cursor.execute()


