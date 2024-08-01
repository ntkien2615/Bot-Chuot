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

        if user.id == 1042729081088778272:
            await interaction.response.send_message('Làm sao t hack chính tôi đc, thử ai đó đi')

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
        opr = self.random_file_read('./txt_files/hack/2b_computer_opr.txt')
        await asyncio.sleep(1)
        await interaction.edit_original_response(content=f'Đăng nhập thành công, máy tính {user} đang chạy trên hệ điều hành: {opr}')
        await asyncio.sleep(1)
        #End fake attacking computer

        #Fake sending image
        await interaction.edit_original_response(content=f'Đang truy cập vào thư mục ảnh...')
        await asyncio.sleep(1)
        anh = self.random_file_read('./txt_files/hack/3a_img.txt')
        anh_embed = discord.Embed(title="", description="", color=discord.Color.red())
        anh_embed.set_image(url=anh)
        await interaction.edit_original_response(content=f'Thành công, hình ảnh gần đây nhất của {user}: ',embed=anh_embed)
        await asyncio.sleep(3)

        #Discord
        await interaction.edit_original_response(content=f'Đang truy cập vào discord:...', embed=None)
        await asyncio.sleep(1)
        discord_message = self.random_file_read('./txt_files/hack/3b_discord_message.txt')
        await interaction.edit_original_response(content=f'Phát hiện tin nhắn gần đây nhất của {user}: {discord_message}',embed=None)
        await asyncio.sleep(1)

        #Facebook
        await interaction.edit_original_response(content=f'Đang truy cập vào Facebook:...',embed=None)
        await asyncio.sleep(1)
        await interaction.edit_original_response(content=f'Đang tìm kiếm bình luận gần đây...')
        await asyncio.sleep(1)
        await interaction.edit_original_response(content='Phát hiện bình luận')
        await interaction.edit_original_response
        facebook_comment = self.random_file_read('./txt_files/hack/3c_facebook_comment.txt')
        await interaction.edit_original_response(content=f'Nội dung: {facebook_comment}')
        await asyncio.sleep(1)

        #Messenger
        await interaction.edit_original_response(content='Đang truy cập vào Messenger...')
        await asyncio.sleep(1)
        await interaction.edit_original_response(content='')
         for i in range(5, 0, -1):
            await interaction.edit_original_response(content=f"Đang tìm tin nhắn có theme của setlove... {i} seconds remaining")
            await asyncio.sleep(1)
        a = random.randint(1,2)
        if a == 1:
            await interaction.edit_original_response(content="Không phát hiện, có lẽ mục tiêu không có bạn gái")
            await asyncio.sleep(1)
        else:
            await interaction.edit_original_response(content='Đã phát hiện, tiến hành gửi tin nhắn với nội dung: Cút mẹ mày đi')
            await asyncio.sleep(1)
            await interaction.edit_original_response(content='Đã spam tin nhắn, tiến hành block các tài khoản')
            await asyncio.sleep(1)

        #Google_search
        await interaction.edit_original_response(content='Đang truy cập vào Google Activity...')
        await asyncio.sleep(1)
        await interaction.edit_original_response(content='Đang tìm kiếm hoạt động gần đây...')
        for i in range(3, 0, -1):
            await interaction.edit_original_response(content=f"Đang tìm lịch sử tin nhắn gần đây... {i} seconds remaining")
            await asyncio.sleep(1)
        search = self.random_file_read('./txt_files/hack/3d_google_search.txt')
        await interaction.edit_original_response(content=f'Tìm thành công, lần gần đây {user} có đã tìm kiếm: {search}')
        await asyncio.sleep(2)

        #Ending
        interaction.edit_original_response(content='đang thu thập tất cả thông tin tìm được')
        await asyncio.sleep(1)

        b = random.randint(1,5)
        if b == 1:
            await interaction.edit_original_response(content='Đã thu thập các thông tin cá nhân nhạy cảm')
            await asyncio.sleep(1)
            await interaction.edit_original_response(content='Đăng đăng lên bán...')
            await asyncio.sleep(3)
            await interaction.edit_original_response(content='Bán thành công! Tôi được 10$')
            await asyncio.sleep(1)
            await interaction.edit_original_response(content='Tạo backdoor và xóa sạch dấu vết:...')
            await asyncio.sleep(3)
            await interaction.edit_original_response(content='Đang thoát...')
            await asyncio.sleep(1)
            await interaction.edit_original_response(content='Hoàn thành!')
        elif b == 2:
            await interaction.edit_original_response(content='Xóa sạch dữ liệu: ')
            for i in range(1,10):
                await interaction.edit_original_response(content=f'Xóa sạch dữ liệu: {i*10} %') 
                await asyncio.sleep(0.2)
            await asyncio.sleep(1)
            await interaction.edit_original_response(content='BỤP!!!!!!!!!!')
            await asyncio.sleep(1.5)
        elif b == 3:
            await interaction.edit_original_response(content='Gửi đến ở đâu đó ở Trung Đông')
            await asyncio.sleep(1)
            await interaction.edit_original_response(content='Có người nhắn lại: "Haram"')
            await asyncio.sleep(1)
            await interaction.edit_original_response(content='Có tin nhắn: Đã định vị tên lửa vào vị trí')
            await asyncio.sleep(1)
            await interaction.edit_original_response(content='Tạm biệt!')
            await asyncio.sleep(1)
        elif b == 4:
            await interaction.edit_original_response(content='Gửi đến Nga')
            await asyncio.sleep(1)
            await interaction.edit_original_response(content='Thôi xong, trốn trước đây')
            await asyncio.sleep(1)
            await interaction.edit_original_response(content='Bye!!!!')
            await asyncio.sleep(1)
        await interaction.edit_original_response(content=f"Hack complete! Đã thực hiện cuộc tấn công đầy nguy hiểm vào máy tính <@{user.id}>", embed=None)

async def setup(bot)
    await bot.add_cog(Hack(bot))
