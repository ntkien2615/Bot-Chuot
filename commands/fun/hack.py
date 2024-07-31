import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import random

class Hack(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='hack',description='hack vào máy ai đó')
    @app_commands.describe(user='máy tính của ai')
    async def hack(self,interaction:discord.Interaction,user:discord.Member):
        if user == interaction.user:
            await interaction.response.send_message("Ông không thể hack chính ông đc, thử đứa khác đi")
            return

        await interaction.response.send_message(f"Bắt đầu thực hiện việc hack nguy hiểm vào máy tính của <@{user.id}>...")
        await asyncio.sleep(1)

        for i in range(5, 0, -1):
            await interaction.edit_original_response(content=f"Tìm kiếm wifi của <@{user.id}: {i} seconds remaining...")
            await asyncio.sleep(1)  # Use asyncio.sleep for non-blocking delays

        await interaction.edit_original_response(content=f'Phát hiện wifi của <@{user.id}>')
        await asyncio.sleep(1)

        def random_file_read(self, file_path):
        try:
            with open(file_path, "r") as f:
                lines = f.readlines()
            if lines:
                return random.choice(lines).strip()
        except (IndexError, FileNotFoundError) as e:
            return None

        wifi_name = random_file_read('./txt_files/hack/1a_wifiname.txt')
        number_connected = random.randint(1,9)
        await interaction.edit_original_response(content=f'Tên wifi: {wifi_name}, có {number_connected} kết nối')
        await interaction.edit_original_response(content=f'Bắt đầu WPA Handshake...')
        await asyncio.sleep(2)
        wifi_pass = random_file_read('./txt_files/hack/1b_wifipass.txt')
        await interaction.edit_original_response(content=f'Thành công, password là: {wifi_pass}')
        await asyncio.sleep(1)
        # Conclude with a humorous message
        await interaction.edit_original_response(content=f"Hack complete! <@{user.id}>'s computer is now filled with... confetti! ")

async def setup(bot):
    await bot.add_cog(Hack(bot))
