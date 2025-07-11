import discord
from discord.ext import commands
from discord import app_commands
import random

from src.commands.base_command import FunCommand


class Kill(FunCommand):
    def __init__(self, discord_bot):
        super().__init__(discord_bot)

    @app_commands.command(name='kill',description='kill ai đó')
    @app_commands.describe(user='tên người bạn muốn kill')
    async def kill(self,interaction:discord.Interaction,user: discord.Member):
        if user == interaction.user:
            await interaction.response.send_message('Đừng tự giết mình như thế dum dum')
        elif user.id == 1042729081088778272:
            await interaction.response.send_message('Hey, gì chơi kì zậy?')
        else:
            kill_list = [
            'c^m khi xem sẽ quá nhiều',
            'lỡ đập Bạc Fluminat trong khi tưởng là đá', 'xem nhầm acn cosplay',
            'dùng meth quá mức', 'bị mẹ gank', 'đơn giản là bị đánh',
            'không rõ lí do :))))', 'FBI bắt', '"em yêu thằng bạn thân của anh"' ,
            'bị trùm trường túm đầu', 'máy tính mới build nổ sấp mặt',
            'mở nhầm bài tập về nhà trước mặt phụ huynh',
            'bị một thằng rat bắn chết khi đang qwerty trong nhà',
            'học theo cách làm c4 trên top top',
            'ảo tưởng lên cân 5',
            'chơi game 159 phút 99s',
            'bồ đá','đi làm vào ngày 11/9/2001',
            'làm công nhân ở Chernobyl trong ngày 25/4/1986',
            'đi làm việc ở Hiroshma 6/8/1945',
            'đi làm ở Nagasaki 9/8/1945','chơi buckshot roullete'
        ]
        kill_list_random = random.choice(kill_list)
        await interaction.response.send_message(f'<@{user.id}> đã chết bởi lý do: {kill_list_random}')

