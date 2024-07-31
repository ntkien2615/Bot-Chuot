import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import random

class Hack(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def random_file_read(self, file_path):
            try:
                with open(file_path, "r") as f:
                    lines = f.readlines()
                if lines:
                    return random.choice(lines).strip()
            except (IndexError, FileNotFoundError) as e:
                return None

    @app_commands.command(name='hack',description='hack vào máy ai đó (beta)')
    @app_commands.describe(user='máy tính của ai')
    async def hack(self,interaction:discord.Interaction,user:discord.Member):
        if user == interaction.user:
            await interaction.response.send_message("Ông không thể hack chính ông đc, thử đứa khác đi")
            return

        await interaction.response.send_message(f"Bắt đầu thực hiện việc hack nguy hiểm vào máy tính của <@{user.id}>...")
        await asyncio.sleep(1)
        
        #fake attacking Wifi
        for i in range(5, 0, -1):
            await interaction.edit_original_response(content=f"Tìm kiếm wifi của <@{user.id}>: {i} seconds remaining...")
            await asyncio.sleep(1)  # Use asyncio.sleep for non-blocking delays

        await interaction.edit_original_response(content=f'Phát hiện wifi của <@{user.id}>')
        await asyncio.sleep(1)

        wifi_name = self.random_file_read('./txt_files/hack/1a_wifiname.txt')
        number_connected = random.randint(1,9)
        await interaction.edit_original_response(content=f'Tên wifi: {wifi_name}, có {number_connected} kết nối')
        await asyncio.sleep(3)

        await interaction.edit_original_response(content=f'Bắt đầu WPA Handshake...')
        await asyncio.sleep(1)
        for i in range(5, 0, -1):
            await interaction.edit_original_response(content=f"Bắt đầu WPA Handshake... {i} seconds remaining")
            await asyncio.sleep(1)

        wifi_pass = self.random_file_read('./txt_files/hack/1b_wifipass.txt')
        await interaction.edit_original_response(content=f'Thành công, password là: {wifi_pass}')
        await asyncio.sleep(3)
        #end fake attacking Wifi

        #Fake attacking Computer Password
        await interaction.edit_original_response(content=f'Bắt đầu tìm kiếm máy tính của {user}:')
        await asyncio.sleep(1)
        for i in range(5, 0, -1):
            await interaction.edit_original_response(content=f"Bắt đầu tìm kiếm máy tính của {user}: {i} seconds remaining")
            await asyncio.sleep(1)
        computer_username = self.random_file_read('./txt_files/hack/2a_computer_name.txt')
        await interaction.edit_original_response(content=f'Thành công, tên đăng nhập là: {computer_username}')
        await asyncio.sleep(1)
        await interaction.edit_original_response(content=f'Đang bẻ khóa...')
        for i in range(5, 0, -1):
            await interaction.edit_original_response(content=f"Đang bẻ khóa... {i} seconds remaining")
            await asyncio.sleep(1)
        computer_pass = self.random_file_read('./txt_files/hack/2c_computer_pass.txt')
        await interaction.edit_original_response(content=f'Thành công: pass là {computer_pass}')
        opr = self.random_file_read('./txt_files/hack/2b_computer_opr')
        await interaction.edit_original_response(content=f'Đăng nhập thành công, máy tính {user} đang chạy trên hệ điều hành:{opr}')
        #End fake attacking computer

        #Fake sending image
        await interaction.edit_original_response(content=f'Đang truy cập vào thư mục ảnh...')
        await asyncio.sleep(1)
        anh = self.random_file_read('./txt_files/hack/3a_img.txt')
        anh_embed = discord.Embed(title="", description="", color=discord.Color.red())
        anh_embed.set_image(url=anh)
        await interaction.edit_original_response(content=f'Thành công, hình ảnh gần đây nhất: ',embed=anh_embed)
        await asyncio.sleep(1)

        await interaction.edit_original_response(content=f"Hack complete! Đã thực hiện cuộc tấn công đầy nguy hiểm vào máy tính <@{user.id}>")

async def setup(bot):
    await bot.add_cog(Hack(bot))
