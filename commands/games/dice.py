from discord.ext import commands
import random


class dice(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def coinflip(self, ctx):
        coin = random.randint(1, 2)
        if coin == 1:
            mat = 'mặt ngửa'
        else:
            mat = 'mặt sấp'

        await ctx.send('tung đồng xu 2 mặt được: ' + mat)
        return

    @commands.command()
    async def dice(self, ctx, number: int):
        if number < 0:
            await ctx.send('xin lỗi, thứ bạn cần không thuộc về thế giới này')
            return

        if number == 0:
            await ctx.send('Really? Bạn muốn tôi dice một con xúc sắc 0 mặt?')
            return

        platon = [2, 4, 6, 8, 12, 20]

        if number not in platon:
            await ctx.send(
                'well, tôi đã được thay đổi dể tuân theo khối đa diện đều platon (4,6,8,12,20) :)))))'
            )
            return
        else:
            number_random = random.randint(1, number)

        await ctx.send(f'Kết quả từ xúc sắc {number} mặt: {number_random}')


async def setup(bot):
    await bot.add_cog(dice(bot))
