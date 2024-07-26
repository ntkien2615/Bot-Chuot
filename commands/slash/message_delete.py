import discord
from discord.ext import commands
from discord import app_commands


class delslash(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='msg_delete', description='Xóa tin nhắn')
    @commands.has_permissions(manage_messages=True)
    async def msgdeleteslash(self,interaction: discord.Interaction,message_interaction:discord.InteractionMessage,ammount: int):
        try:
            if amount > 100:
                await interaction.response.send_message("Bro tôi không xóa nổi 100 tin nhắn đâu", ephemeral=True)
            return
            for i in range(1,ammount):
                await message_interaction.channel.delete()
            embed = discord.Embed(title="", description=f"{ammount} tin nhắn đã boom by A-train", color=discord.Color.random())
            embed.set_image(url="https://tenor.com/view/a-train-edit-a-train-the-boys-a-train-the-boys-edit-gif-26341809")
            await interaction.send_message(Embed=embed, ephemeral=True)
        except Exception as e:
            print(e)


async def setup(bot):
    await bot.add_cog(delslash(bot))
