from discord.ext import commands
# import os


class on_command_error(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            msg = str(
                'Bạn đừng spam câu lệnh này nữa vì đơn giản không có câu lệnh này, nếu muốn góp ý thì liên hệ admin.')
            # Indent this line
            await ctx.reply(msg, mention_author=False, delete_after=10.0)
        return

    # os.system('cls' if os.name == 'nt' else 'clear')


async def setup(bot):
    await bot.add_cog(on_command_error(bot))
