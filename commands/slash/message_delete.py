import discord
from discord.ext import commands
from discord import app_commands


class delslash(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='msg_delete', description='Xóa tin nhắn')
    @commands.has_permissions(manage_messages=True)
    async def msgdeleteslash(self,interaction: discord.Interaction,amount: int):
        if amount > 100:
            await interaction.response.send_message("Bro tôi không xóa nổi 100 tin nhắn đâu", ephemeral=True)
        return
        try:
            deleted = await message_interaction.channel.purge(limit=amount, before=message_interaction)
            embed = discord.Embed(title="", description=f"{len(deleted)} tin nhắn đã được xóa bởi A-Train ({amount} messages deleted by A-Train)", color=discord.Color.random())
            embed.set_image(url="https://tenor.com/view/a-train-edit-a-train-the-boys-a-train-the-boys-edit-gif-26341809")
            await interaction.channel.send(embed=embed)
        except discord.HTTPException as e:
            print(f"An error occurred while deleting messages: {e}")
            await interaction.response.send_message("Có lỗi xảy ra khi xóa tin nhắn (Error deleting messages)", ephemeral=True)
        except Exception as e:
            print(f"Unexpected error: {e}")
            await interaction.response.send_message("Đã xảy ra lỗi không mong đợi (Unexpected error occurred)", ephemeral=True)


async def setup(bot):
    await bot.add_cog(delslash(bot))
