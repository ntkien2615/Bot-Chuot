import discord
import random
from discord.ext import commands


from src.commands.base_command import PrefixCommand


class wibi(PrefixCommand):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    async def wibi(self, ctx, member: discord.Member,):
        wibi = [
            f'ngắm nhìn và tương tác với một tờ giấy vô tri thích không <@{member.id}> ?',
            f'mặc dù tao rất ghét trẻ con nhưng cho bọn chúng vào phòng chứa đầy ảnh cái mày gọi là ghệ mày là niềm hạnh phúc của tao đấy <@{member.id}>',
            f'Hmm? Tại sao m càng già nhưng vợ m y như cũ? Đó là vì vợ m chỉ là một tờ giấy lộn thôi <@{member.id}>',
            f'Không sao đâu <@{member.id}>, con loli bạn thích chỉ {random.randint(500,10000)} tuổi thôi lmfao',
            f'Thử tưởng tượng m, <@{member.id}> đang simp một con loli 46 tuổi (ví dụ thôi, lỡ m simp một con khác tương tự thì sao? kkkk)'
        ]

        wibi_list_random = random.choice(wibi)
        if member.id == ctx.author.id:
            await ctx.send('well lần đầu tiên có người tự nhận mình là đáy xh sau đạt 7 chữ')
            await ctx.send('https://images-ext-1.discordapp.net/external/wVbLexoDkusxANA5oX62wkVw7GF5uXuVT18DvKUumJw/%3Frik%3D763YgHcEGIXBew%26pid%3DImgRaw%26r%3D0/https/th.bing.com/th/id/R.2ea001ce82210771c00f73500d7e97cd?width=1202&height=676')
            return
        if member.id == 868475751459094580 or member.id == 893468716694667275:
            await ctx.send('bạn không thể nói người này là wibi được, ||đúng là thằng lờ wibi||')
            return
        if member.id == 1042729081088778272:
            await ctx.message.delete()
            await ctx.send(f'bạn cũng khá thông minh đấy {ctx.author.mention}, nhưng còn hơi non', delete_after=2.0)
            return
        if member.id == 845123446550560779:
            await ctx.send(wibi[3])
            return
        else:
            await ctx.send(wibi_list_random)

        if wibi_list_random == wibi[4]:
            await ctx.send('https://media.discordapp.net/attachments/1077151202040614988/1077255610539708508/281.png')

    @wibi.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.message.delete()
            msg = f'<@{ctx.author.id}> Cay lắm đúng không, ĐỪNG SPAM NỮA, ĐỢI SAU : {error.retry_after:.2f} s.'
            await ctx.send(msg, delete_after=2.0)
        else:
            # Xử lý các lỗi khác nếu cần
            pass
