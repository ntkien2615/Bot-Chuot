import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import random
import os

from src.commands.base_command import FunCommand


class Hack(FunCommand):
    def __init__(self, discord_bot):
        super().__init__(discord_bot)
        self.base_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'txt_files', 'hack')

    def random_file_read(self, file_name):
        file_path = os.path.join(self.base_dir, file_name)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            if lines:
                return random.choice(lines).strip()
        except (IndexError, FileNotFoundError) as e:
            print(f"Error in random_file_read: {e}")
            return None

    async def countdown(self, interaction, message, seconds):
        for i in range(seconds, 0, -1):
            await interaction.edit_original_response(content=f"{message} {i} seconds remaining...")
            await asyncio.sleep(1)

    @app_commands.command(name='hack', description='hack vào máy ai đó (beta)')
    @app_commands.describe(user='máy tính của ai')
    async def hack(self, interaction: discord.Interaction, user: discord.Member = None):
        if user is None:
            await interaction.response.send_message("Hãy chọn người để hack", ephemeral=True)
            return
            
        if user == interaction.user:
            await interaction.response.send_message("Ông không thể hack chính ông đc, thử đứa khác đi")
            return

        if user.id == 1042729081088778272:
            await interaction.response.send_message('Làm sao t hack chính tôi đc, thử ai đó đi')
            return

        await interaction.response.send_message(f"Bắt đầu thực hiện việc hack nguy hiểm vào máy tính của <@{user.id}>...")
        await asyncio.sleep(2)
        
        # Fake attacking Wifi
        await self.countdown(interaction, f"Tìm kiếm wifi của <@{user.id}>:", 5)
        await interaction.edit_original_response(content=f'Phát hiện wifi của <@{user.id}>')
        await asyncio.sleep(2)

        wifi_name = self.random_file_read('1a_wifiname.txt')
        number_connected = random.randint(1, 9)
        await interaction.edit_original_response(content=f'Tên wifi: {wifi_name}, có {number_connected} kết nối')
        await asyncio.sleep(3)

        await interaction.edit_original_response(content=f'Bắt đầu WPA Handshake...')
        await self.countdown(interaction, "Bắt đầu WPA Handshake...", 5)

        wifi_pass = self.random_file_read('1b_wifipass.txt')
        await interaction.edit_original_response(content=f'Thành công, password là: {wifi_pass}')
        await asyncio.sleep(3)
        # End fake attacking Wifi

        # Fake attacking Computer Password
        await interaction.edit_original_response(content=f'Bắt đầu tìm kiếm máy tính của {user}:')
        await self.countdown(interaction, f"Bắt đầu tìm kiếm máy tính của {user}:", 5)
        computer_username = self.random_file_read('2a_computer_name.txt')
        await interaction.edit_original_response(content=f'Thành công, tên đăng nhập là: {computer_username}')
        await asyncio.sleep(2)
        await interaction.edit_original_response(content=f'Đang bẻ khóa...')
        await self.countdown(interaction, "Đang bẻ khóa...", 5)
        computer_pass = self.random_file_read('2c_computer_pass.txt')
        await interaction.edit_original_response(content=f'Thành công: pass là {computer_pass}')
        opr = self.random_file_read('2b_computer_opr.txt')
        await asyncio.sleep(2)
        await interaction.edit_original_response(content=f'Đăng nhập thành công, máy tính {user} đang chạy trên hệ điều hành: {opr}')
        await asyncio.sleep(2)
        # End fake attacking computer

        # Fake sending image
        await interaction.edit_original_response(content=f'Đang truy cập vào thư mục ảnh...')
        await asyncio.sleep(2)
        anh = self.random_file_read('3a_img.txt')
        anh_embed = discord.Embed(title="", description="", color=discord.Color.red())
        anh_embed.set_image(url=anh)
        await interaction.edit_original_response(content=f'Thành công, hình ảnh gần đây nhất của {user}: ', embed=anh_embed)
        await asyncio.sleep(3)

        # Discord
        await interaction.edit_original_response(content=f'Đang truy cập vào discord:...', embed=None)
        await asyncio.sleep(2)
        discord_message = self.random_file_read('3b_discord_message.txt')
        await interaction.edit_original_response(content=f'Phát hiện tin nhắn gần đây nhất của {user}: {discord_message}', embed=None)
        await asyncio.sleep(2)

        # Facebook
        await interaction.edit_original_response(content=f'Đang truy cập vào Facebook:...', embed=None)
        await asyncio.sleep(2)
        await interaction.edit_original_response(content=f'Đang tìm kiếm bình luận gần đây...')
        await asyncio.sleep(2)
        await interaction.edit_original_response(content='Phát hiện bình luận')
        facebook_comment = self.random_file_read('3c_facebook_comment.txt')
        await interaction.edit_original_response(content=f'Nội dung: {facebook_comment}')
        await asyncio.sleep(2)

        # Messenger
        await interaction.edit_original_response(content='Đang truy cập vào Messenger...')
        await asyncio.sleep(2)
        await self.countdown(interaction, "Đang tìm tin nhắn có theme của setlove...", 5)
        a = random.randint(1, 2)
        if a == 1:
            await interaction.edit_original_response(content="Không phát hiện, có lẽ mục tiêu không có bạn gái")
            await asyncio.sleep(2)
        else:
            await interaction.edit_original_response(content='Đã phát hiện, tiến hành gửi tin nhắn với nội dung: Cút mẹ mày đi')
            await asyncio.sleep(3)
            await interaction.edit_original_response(content='Đã spam tin nhắn, tiến hành block các tài khoản')
            await asyncio.sleep(2)

        # Google_search
        await interaction.edit_original_response(content='Đang truy cập vào Google Activity...')
        await asyncio.sleep(2)
        await interaction.edit_original_response(content='Đang tìm kiếm hoạt động gần đây...')
        await self.countdown(interaction, "Đang tìm lịch sử tin nhắn gần đây...", 3)
        search = self.random_file_read('3d_google_search.txt')
        await interaction.edit_original_response(content=f'Tìm thành công, lần gần đây {user} có đã tìm kiếm: {search}')
        await asyncio.sleep(2)

        # Ending
        await interaction.edit_original_response(content='đang thu thập tất cả thông tin tìm được')
        await asyncio.sleep(2)

        b = random.randint(1, 4)
        if b == 1:
            await interaction.edit_original_response(content='Đã thu thập các thông tin cá nhân nhạy cảm')
            await asyncio.sleep(2)
            await interaction.edit_original_response(content='Đăng đăng lên bán...')
            await asyncio.sleep(3)
            await interaction.edit_original_response(content='Bán thành công! Tôi được 10

async def setup(bot):
    await bot.add_cog(Hack(bot))
