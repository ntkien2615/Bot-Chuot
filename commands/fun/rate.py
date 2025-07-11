import discord
from discord.ext import commands
from discord import app_commands
import random


from commands.base_command import FunCommand


class rateslash(FunCommand):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='rate',
                          description='rate thử bạn trông như thế nào?')
    @app_commands.describe(member='Người bạn muốn đánh giá', type='chọn các phương châm để đánh giá')
    @app_commands.choices(type=[
        discord.app_commands.Choice(name="Gay", value="Gay"),
        discord.app_commands.Choice(name="Độ best toán", value="Toán"),
        discord.app_commands.Choice(name="Độ best lý", value="Lý"),
        discord.app_commands.Choice(name="Độ best hóa", value="Hóa"),
        discord.app_commands.Choice(name="Game", value="Game"),
        discord.app_commands.Choice(name="Soviet", value="Soviet"),
        discord.app_commands.Choice(name="Wibu", value="Wibu"),
        discord.app_commands.Choice(name="Simp", value="Simp"),
        discord.app_commands.Choice(name="Nerd", value="Nerd")
    ])
    async def rate(self, interaction: discord.Interaction,
                        member: discord.Member = None, type: str = None):
        if member is None:
            member = interaction.user
        
        embed_msg = discord.Embed(
            title="RATE r43 BETA", color=discord.Color.random())

        percent = random.randint(0, 100)
        
        match type:
            case "Gay":
                embed_msg.add_field(name="",
                                    value=f"{member} có {percent} % gay",
                                    inline=False)
                if percent > 50:
                    lgbt = ['https://media.discordapp.net/attachments/1077255654512787537/1145686809616064553/IMG_2531.JPG', 'https://media.discordapp.net/attachments/1077255654512787537/1145686848237228123/IMG_2545.JPG?width=841&height=676', 'https://media.discordapp.net/attachments/1077255654512787537/1145686837277491291/IMG_2534.JPG',
                            'https://media.discordapp.net/attachments/1077255654512787537/1145686810584952883/IMG_2526.JPG', 'https://media.discordapp.net/attachments/1077255654512787537/1145686811084070932/IMG_2528.JPG', 'https://media.discordapp.net/attachments/883268139922636820/1148243583867027456/375059363_778041907410216_194594058113567294_n.png']
                    embed_msg.set_image(url=random.choice(lgbt))
                embed_msg.set_footer(text=f"Rated by {interaction.user}",
                                    icon_url=interaction.user.avatar)
            case "Wibu":
                embed_msg.add_field(name="",
                                    value=f"{member} có {percent} % Wibu",
                                    inline=False)
                if percent > 60:
                    embed_msg.set_image(
                        url='https://media.discordapp.net/attachments/1077255654512787537/1146450773945897030/filthy-frank-papa-franku.gif')
                embed_msg.set_footer(text=f"Rated by {interaction.user}",
                                    icon_url=interaction.user.avatar)
            case "Soviet":
                embed_msg.add_field(
                    name="",
                    value=f"{member} có {random.randint(0,100)} % Soviet",
                    inline=False)
                embed_msg.set_footer(text=f"Rated by {interaction.user}")
            case "Toán" | "Lý" | "Hóa":
                ratemon = [
                    'Thằng gà 0đ', 'Vật lộn từng điểm 2', 'Nhân vật alimi 5 điểm',
                    'Tạm ổn 7,8', 'vip pro 9,10', 'đội tuyển hsg',
                    'đội tuyển hsg nhưng rớt môn', 'cục vàng server'
                ]
                embed_msg.add_field(
                    name="",
                    value=f"{member} có thông thạo môn {type} cỡ: {random.choice(ratemon)}",
                    inline=False)
                embed_msg.set_footer(text=f"Rated by {interaction.user}",
                                    icon_url=interaction.user.avatar)
            case "Game":
                rategame = [
                    'thằng gà mờ', 'ông trùm phi phai', 'troll game', 'cày thuê',
                    'ĐẠN THẦN QUANGGGGGGGGGGGGGGGGG',
                    'vẩy awm như vẩy rau, quick scope, no scope, lướt và scope',
                    'cục vàng server', 'ĐỬNG CÓ T* T*', 'bình thường',
                    'chơi vì bồ cũng chơi', 'chơi vì không có bồ :(',
                    'mất quyền kiểm soát, mất quyền kiểm soát',
                    'edit giựt giựt mù mắt người xem', 'elsu mafia', 'youtuber',
                    'tóp tóp trẻ trâu er', 'sao có thằng nói tiếng nga cầm ak47 6x kia?',
                    'chơi kiếm bồ', 'chơi giả trap lừa được skin', 'bị lừa pay acc',
                    'vung tay quá trán, skin chất đầy nhà', 'Anh là tay to', 'Hacker',
                    '5 phút 1 trận', 'Hacker nhưng đợi 70 năm nữa', 'Bị trap lừa pay tiền',
                    'sóc vàng aya', 'sóc vàng wibu', 'chơi vì ghệ ảo'
                ]
                embed_msg.add_field(
                    name="",
                    value=f"Vai trò của {member} trong game là : {random.choice(rategame)}",
                    inline=False)
                embed_msg.set_footer(text=f"Rated by {interaction.user}",
                                    icon_url=interaction.user.avatar)
            case "Simp":
                embed_msg.add_field(name="",
                                    value=f"{member} có {random.randint(0,100)} % Simp",
                                    inline=False)
                embed_msg.set_footer(text=f"Rated by {interaction.user}",
                                    icon_url=interaction.user.avatar)
            case "Nerd":
                nerdpercent = random.randint(0, 100)
                embed_msg.add_field(name="",
                                    value=f"{member} có {nerdpercent} % Nerd",
                                    inline=False)
                if nerdpercent > 60:
                    embed_msg.add_field(
                        name="", value="NERD DETECTED", inline=False)
                    embed_msg.set_image(
                        url='https://media.discordapp.net/attachments/883268139922636820/1144988661105053768/371459651_323564320152104_2701977404234363223_n.png')
                embed_msg.set_footer(text=f"Rated by {interaction.user}",
                                    icon_url=interaction.user.avatar)
            case _:
                embed_msg.add_field(name="",
                                   value=f"Vui lòng chọn loại đánh giá",
                                   inline=False)

        await interaction.response.send_message(embed=embed_msg)
