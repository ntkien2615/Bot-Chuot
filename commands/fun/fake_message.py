import discord
from discord.ext import commands
from discord import app_commands


from commands.base_command import FunCommand


class fakemsgslash(FunCommand):

    def __init__(self, bot):
        super().__init__(bot)

    @app_commands.command(name='fakemsg', description='gửi tin nhắn giả với tên của người khác')
    @app_commands.describe(member="Người muốn fake tin nhắn")
    @app_commands.describe(msg="Tin nhắn giả")
    async def fakemsg(self, interaction: discord.Interaction,member:discord.Member,msg: str):
        if not member:
            author_name = interaction.user.name
            author_avatar = interaction.user.avatar.url
        else:
            try:
                author_name = member.name
                author_avatar = member.avatar.url
            except discord.HTTPException as e:
                if e.status == 403:
                    await interaction.response.send_message("Tui ko có quyền lmfao, sorry.", ephemeral=True)
                    return
                else:
                    raise 
        try:
            webhook = await interaction.channel.create_webhook(name=f"Simulated Message - {author_name}")
            await webhook.send(msg, username=author_name, avatar_url=author_avatar)
            await webhook.delete()
            await interaction.response.send_message("Thành công!",ephemeral=True)
        except discord.Forbidden as e:
            await interaction.response.send_message("I don't have permission to create webhooks in this channel.", ephemeral=True)
        except discord.HTTPException as e:
            print(f"An error occurred while creating a webhook: {e}")
            await interaction.response.send_message("An error occurred while simulating the message. Please try again later.", ephemeral=True)