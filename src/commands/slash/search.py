import discord, os
from discord.ext import commands
from discord import app_commands
import random
from googleapiclient.discovery import build
from dotenv import load_dotenv, find_dotenv

from src.commands.base_command import SlashCommand


class searchslash(SlashCommand):

    category = "utility"

    def __init__(self, discord_bot):
        super().__init__(discord_bot)
        self.bot = discord_bot.bot

    @app_commands.command(name='search', description='tìm ảnh trên mạng')
    @app_commands.describe(search='bạn search cái gì')
    async def search(self, interaction: discord.Interaction, search: str):
        load_dotenv(find_dotenv())
        api_key = os.getenv("search_api_key")
        ran = random.randint(0, 9)
        resource = build('customsearch', 'v1', developerKey=api_key).cse()
        result = resource.list(q=f"{search}",
                               cx="61b1f208600dd44d6",
                               searchType="image").execute()
        url = result["items"][ran]["link"]
        await interaction.response.send_message(url)
