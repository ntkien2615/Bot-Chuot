import discord
from discord.ext import commands, tasks
from itertools import cycle


class actvity(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.status = cycle([
            'Chẳng giữ những lời hứa, lúc xưa từng hẹn thề',
            'Đón đưa cùng người về, những nơi mà ta êm ấm',
            'Lời chia tay em nói, thế thôi đành ngậm ngùi',
            'Lẻ loi nhìn người yên vui cùng ai',
            'Ngồi ôm bao nỗi nhớ, ngẩn ngơ vẫn đợi chờ',
            'Giấc mơ lụi tàn, để con tim lặng im vỡ nát',
            'Giờ hai ta hai hướng, nhớ thương còn lại gì',
            'Vấn vương cũng chẳng níu em đừng đi !',
            'Tại sao anh còn thương em mãi',
            'Nhưng lòng đau thì ai có hay ?',
            'Người đi người buông ai thấu đâu',
            'Khi tình ta giờ chia hai ngã',
            'Là em đã rời xa anh đấy',
            'Để tình tan còn bao đắng cay',
            'Chẳng câu biệt ly em bước đi',
            'Theo người ta em không suy nghĩ',
            'Vì ai em vội quên năm tháng',
            'Kỷ niệm xưa giờ đây trái ngang',
            'Để cho nước mắt còn rơi trên',
            'Đôi bờ mi mà sao em nỡ ?',
            'Lòng còn vương đem lời thương chôn giấu',
            'Bao đậm sâu giờ cũng đớn đau',
            'Đành tâm nhìn em hạnh phúc',
            'Những ngọt ngào em trao cho người ta !'
        ])

    @tasks.loop(seconds=5.0)
    async def change_status(self):
        await self.bot.change_presence(status=discord.Status.online,
                                       activity=discord.Activity(
                                           type=discord.ActivityType.watching,
                                           name=next(self.status)))

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        self.change_status.start()


async def setup(bot):
    await bot.add_cog(actvity(bot))
