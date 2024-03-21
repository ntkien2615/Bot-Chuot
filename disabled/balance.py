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

        db = aiosqlite.connect("./db/main.sqlite")
        cursor = db.cursor()

        cursor.execute()


