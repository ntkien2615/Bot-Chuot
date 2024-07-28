import discord
from discord.ext import commands
from discord import app_commands
import datetime


class Trongtruonghop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name='trong_truong_hop', description='trong trường hợp nhóm này')

    async def dice(self, interaction: discord.Interaction):
        x = datetime.datetime.now()
        embed = discord.Embed(title="", description=f'Tôi tên là {interaction.user}. Trong trường hợp nhóm này bị điều tra bởi các cơ quan trực thuộc bộ công an (hoặc các tổ chức chính trị tương tự phục vụ cho nhà nước CHXHCNVN), tôi khẳng định mình không liên quan tới nhóm hoặc những cá nhân khác trong nhóm này. Tôi không rõ tại sao mình lại có mặt ở đây vào thời điểm này, có lẽ tài khoản của tôi đã được thêm bởi một bên thứ ba. Tôi cũng xin khẳng định rằng mình không hề giúp sức cho những hành động chống phá Đảng và nhà nước của các thành viên trong nhóm này. Xin cảm ơn!', color=discord.Color.red())
        embed.set_image(url="https://th.bing.com/th/id/OIP.3I9zIQg4SUu9pMO9vZcosQHaEK?rs=1&pid=ImgDetMain")
        await interaction.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(Trongtruonghop(bot))
