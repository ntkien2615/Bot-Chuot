import discord
from discord import app_commands
from discord.ext import commands
import json

class Balance(commands.Cog):  # Capitalize class name for consistency
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="balance", description="Checks your (or someone else's) balance")  # Clearer description
    async def balance(self, interaction: discord.Interaction, member: discord.Member = None):
        if member is None:
            member = interaction.user

        users = await self.get_bank_data()

        # Ensure user data exists before accessing wallet and bank
        if str(member.id) not in users:
            await self.open_account(member)

        wallet = users[str(member.id)]["wallet"]
        bank = users[str(member.id)]["bank"]

        await interaction.response.send_message(f'{wallet} -- {bank}')

    async def open_account(self, member: discord.Member):
        users = await self.get_bank_data()
        if str(member.id) in users:
            return False  # Already has an account

        users[str(member.id)] = {"wallet": 0, "bank": 0}  # Create new entry with initial values

        with open("./balance/balance.json", "w") as f:
            json.dump(users, f)

        return True  # Account created successfully

    async def get_bank_data(self):
        try:
            with open("./balance/balance.json", "r") as f:
                users = json.load(f)
            return users
        except FileNotFoundError:  # Handle missing file gracefully
            return {}  # Return empty dictionary if file doesn't exist

async def setup(bot):
    await bot.add_cog(Balance(bot))  # Use the corrected class name

