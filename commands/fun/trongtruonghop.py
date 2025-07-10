import discord
from discord.ext import commands
from discord import app_commands


from commands.base_command import FunCommand


class Trongtruonghop(FunCommand):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name='trong_truong_hop', description='trong trường hợp nhóm này')

    async def Trongtruonghop(self, interaction: discord.Interaction):
        embed = discord.Embed(title="", description=f'Tôi tên là {interaction.user}. Trong trường hợp nhóm này bị điều tra bởi các cơ quan trực thuộc bộ công an (hoặc các tổ chức chính trị tương tự phục vụ cho nhà nước CHXHCNVN), tôi khẳng định mình không liên quan tới nhóm hoặc những cá nhân khác trong nhóm này. Tôi không rõ tại sao mình lại có mặt ở đây vào thời điểm này, có lẽ tài khoản của tôi đã được thêm bởi một bên thứ ba. Tôi cũng xin khẳng định rằng mình không hề giúp sức cho những hành động chống phá Đảng và nhà nước của các thành viên trong nhóm này. Xin cảm ơn!', color=discord.Color.random())
        embed.set_image(url="https://cdn.discordapp.com/emojis/1029699276953100298.webp?size=128&animated=true")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Trongtruonghop(bot))
