import discord
import random
from discord.ext import commands


class kill(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def kill(self, ctx, member: discord.Member):

        member = member or ctx.author

        kill_list = [
            'c^m khi xem gura quá nhiều',
            'lỡ đập Bạc Fluminat trong khi tưởng là đá', 'xem nhầm acn cosplay',
            'dùng meth quá mức', 'bị mẹ gank', 'đơn giản là bị đánh',
            'không rõ lí do :))))', 'FBI bắt', '"em yêu thằng bạn thân của anh"',
            'bị trùm trường túm đầu', 'máy tính mới build nổ sấp mặt',
            'mở nhầm bài tập về nhà trước mặt phụ huynh'
        ]

        kill_list_random = random.choice(kill_list)
        if member.id == 1042729081088778272:
            await ctx.send('tôi còn yêu đời lắm nhé bro!!!')
            return

        if member.id == ctx.author.id:
            await ctx.send(
                'well, đúng là trên đời có người bi quan đến mức nhờ tôi kill chính mình luôn à?'
            )
            return
        await ctx.send(f'<@{member.id}> đã chết vì: ' + kill_list_random)

        if kill_list_random == kill_list[0]:
            await ctx.send(
                'https://cdn.discordapp.com/attachments/898498537388650536/1073964574929321994/image.png'
            )

        if kill_list_random == kill_list[2]:
            await ctx.send(
                'https://media.discordapp.net/attachments/1081856297785372772/1085059245336170516/323116764_629944388942981_269814954348066558_n.png?width=507&height=676'
            )

        if kill_list_random == kill_list[11]:
            await ctx.send(
                'https://cdn.discordapp.com/attachments/1077255654512787537/1084345403035615382/IMG_2859.jpg',
                delete_after=10)

    @kill.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            msg = f'<@{ctx.author.id}>   Từ từ thôi! Thử lại sau: {error.retry_after:.2f} s.'
        await ctx.send(msg)


async def setup(bot):
    await bot.add_cog(kill(bot))
