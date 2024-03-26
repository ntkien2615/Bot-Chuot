import discord,aiosqlite
from discord import app_commands
from discord.ext import commands
import json

class balance(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @app_commands.command(name="balance",description="xem thử ví bạn (người khác) còn bao nhiêu")
    async def balance(self, interaction:discord.Interaction,member: discord.Member = None):
        if member == None:
            member = interaction.user
        await open_acount(member)
        users = get_bank_data()
        wallet = users[str(user.id)]["wallet"]
        bank = users[str(user.id)]["bank"]
        await interaction.response.send_message(f'{wallet} -- {bank}')
    async def open_acount(user):
        users = get_bank_data()
        if str(user.id) in users:
            return False
        else:
            user[str(user.id)]["wallet"] = 0
            user[str(user.id)]["bank"] = 0
        
        with open("./balance/balance.json","w") as f:
            json.dump(users,f)

        return True
    async def get_bank_data():
        with open("./balance/balance.json","r") as f:
            users = json.load(f)
async def setup(bot):
    await bot.add_cog(balance(bot))


