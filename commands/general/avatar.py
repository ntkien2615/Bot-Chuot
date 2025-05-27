import discord
from discord.ext import commands
from discord import app_commands

class avatarslash(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='avatar', description='lấy avatar của bạn hoặc người khác')
    @app_commands.choices(options=[
        discord.app_commands.Choice(name="Global", value="global", description="Avatar toàn cầu của người dùng"),
        discord.app_commands.Choice(name="Local", value="local", description="Avatar cục bộ của người dùng trong máy chủ")
    ])
    async def avtslash(self, interaction: discord.Interaction, options: str, member: discord.Member = None):
        if member == None:
            member = interaction.user

        if options == 'global':
            embed_msg = discord.Embed(title=f"Avatar global của {member}",
                                    color=discord.Color.random())
            embed_msg.set_author(name=f"{member}",
                                icon_url=member.avatar)
            embed_msg.set_image(url=member.avatar)
            embed_msg.set_footer(text=f"Bởi {interaction.user}",
                                icon_url=interaction.user.avatar)
            await interaction.response.send_message(embed=embed_msg)
        
        if options == 'local':
            try:
                embed_msg = discord.Embed(title=f"Avatar local của {member}",
                                    color=discord.Color.random())
                embed_msg.set_author(name=f"{member}",
                                    icon_url=member.avatar)
                embed_msg.set_image(url=member.guild_avatar.url)
                embed_msg.set_footer(text=f"Bởi {interaction.user}",
                                    icon_url=interaction.user.avatar)
                await interaction.response.send_message(embed=embed_msg)
            except AttributeError:
                await interaction.response.send_message("Người này không có avatar trong máy chủ, có thể người này quá nghèo để có nitro", ephemeral=False)
                return


async def setup(bot):
    await bot.add_cog(avatarslash(bot))
