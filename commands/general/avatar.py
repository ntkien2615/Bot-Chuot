import discord
from discord.ext import commands
from discord import app_commands
from commands.base_command import GeneralCommand


class AvatarCommand(GeneralCommand):
    """Command to get user avatars."""
    
    def __init__(self, bot):
        super().__init__(bot)
        self.name = "avatar"
        self.description = "Lấy avatar của bạn hoặc người khác"

    @app_commands.command(name='avatar', description='lấy avatar của bạn hoặc người khác')
    @app_commands.choices(options=[
        discord.app_commands.Choice(name="Global", value="global", description="Avatar toàn cầu của người dùng"),
        discord.app_commands.Choice(name="Local", value="local", description="Avatar cục bộ của người dùng trong máy chủ")
    ])
    async def avatar(self, interaction: discord.Interaction, member: discord.Member = None, options: str = 'global'):
        try:
            if member is None:
                member = interaction.user

            if options == 'global':
                avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
                embed_msg = discord.Embed(title=f"Avatar global của {member}",
                                        color=discord.Color.random())
                embed_msg.set_author(name=f"{member}",
                                    icon_url=avatar_url)
                embed_msg.set_image(url=avatar_url)
                embed_msg.set_footer(text=f"Bởi {interaction.user}",
                                    icon_url=interaction.user.avatar.url if interaction.user.avatar else interaction.user.default_avatar.url)
                await interaction.response.send_message(embed=embed_msg)
            
            elif options == 'local':
                if member.guild_avatar is None:
                    await interaction.response.send_message("Người này không có avatar trong máy chủ, có thể người này quá nghèo để có nitro", ephemeral=True)
                    return
                
                avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
                embed_msg = discord.Embed(title=f"Avatar local của {member}",
                                        color=discord.Color.random())
                embed_msg.set_author(name=f"{member}",
                                    icon_url=avatar_url)
                embed_msg.set_image(url=member.guild_avatar.url)
                embed_msg.set_footer(text=f"Bởi {interaction.user}",
                                    icon_url=interaction.user.avatar.url if interaction.user.avatar else interaction.user.default_avatar.url)
                await interaction.response.send_message(embed=embed_msg)
        except Exception as e:
            await interaction.response.send_message("Có lỗi xảy ra khi lấy avatar", ephemeral=True)
            print(f"Avatar command error: {e}")


async def setup(bot):
    await bot.add_cog(AvatarCommand(bot))
