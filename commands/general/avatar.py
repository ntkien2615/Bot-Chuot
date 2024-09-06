import discord
from discord.ext import commands
from discord import app_commands

class MyView(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label='test', style=discord.ButtonStyle.grey)
    async def asdf(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message('test success', ephemeral=True)


class avatarslash(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='avatar', description='lấy avatar của bạn hoặc người khác')
    async def avtslash(self, interaction: discord.Interaction, member: discord.Member = None):
        if member == None:
            member = interaction.user

        view = MyView()
        embed_msg = discord.Embed(title=f"Avatar Global của {member}",
                                  color=discord.Color.random())
        embed_msg.set_author(name=f"{member}",
                             icon_url=member.avatar)
        embed_msg.set_image(url=member.avatar)
        embed_msg.set_footer(text=f"Bởi {interaction.user}",
                             icon_url=interaction.user.avatar)
        await interaction.response.send_message(embed=embed_msg, view=view)


async def setup(bot):
    await bot.add_cog(avatarslash(bot))
