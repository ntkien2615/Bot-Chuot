import discord
from discord.ext import commands


class im(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def im(self, ctx, member: discord.Member = None):
        if member == None:
            await ctx.reply('chú phải bắt ai im chứ?')
        else:
            await ctx.send(f'Im nào cô bé <@{member.id}> của tôi')
            await ctx.send(
                'https://media.discordapp.net/attachments/883268139922636820/1125768473595875338/e6328ff4069e2184f8f212fd692ce117.png'
            )


async def setup(bot):
    await bot.add_cog(im(bot))
