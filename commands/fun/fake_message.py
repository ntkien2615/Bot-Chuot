import discord
from discord.ext import commands
from discord import app_commands


class fakemsgslash(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='fakemsg', description='gửi tin nhắn giả với tên của người khác')
    @app_commands.describe(member="Người muốn fake tin nhắn")
    @app_commands.describe(msg="Tin nhắn giả")
    async def fakemsg(self, interaction: discord.Interaction,member:discord.Member,msg: str):
        if member == None:
            await interaction.response.send_message("Có thể nếu bạn không cung cấp tên người nào đó thì mình đã sài tên bạn rồi", ephemeral=True)
            return
        webhook = await interaction.channel.create_webhook(name=member.name)
        await webhook.send(
            str(message), username=member.name, avatar_url=member.avatar_url)

        webhooks = await interaction.channel.webhooks()
        for webhook in webhooks:
                await webhook.delete()
async def setup(bot):
    await bot.add_cog(fakemsgslash(bot))