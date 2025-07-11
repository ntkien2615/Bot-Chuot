import discord
from discord.ext import commands
from discord import app_commands
from src.commands.base_command import GeneralCommand


class UserInfoCommands(GeneralCommand):
    """Commands to get user avatars and banners."""
    
    def __init__(self, discord_bot):
        super().__init__(discord_bot)

    @app_commands.command(name='avatar', description='lấy avatar của bạn hoặc người khác')
    @app_commands.describe(
        member="Thành viên để hiển thị avatar",
        scope="Chọn global hoặc local avatar"
    )
    @app_commands.choices(scope=[
        discord.app_commands.Choice(name="Global", value="global"),
        discord.app_commands.Choice(name="Local", value="local")
    ])
    async def avatar(self, interaction: discord.Interaction, member: discord.Member = None, scope: str = 'global'):
        await interaction.response.defer()
        try:
            if member is None:
                member = interaction.user

            # Fetch the full user object to get all avatar data
            user = await self.bot.fetch_user(member.id)
            
            if scope == 'global':
                avatar_url = user.display_avatar.url
                embed_msg = discord.Embed(
                    title=f"Avatar global của {user.display_name}",
                    color=discord.Color.random()
                )
                embed_msg.set_author(
                    name=user.display_name,
                    icon_url=avatar_url
                )
                embed_msg.set_image(url=avatar_url)
                embed_msg.set_footer(
                    text=f"Bởi {interaction.user.display_name}",
                    icon_url=interaction.user.display_avatar.url
                )
                await interaction.response.send_message(embed=embed_msg)
            
            elif scope == 'local':
                if member.guild_avatar is None:
                    await interaction.response.send_message(
                        "Người này không có avatar trong máy chủ, có thể họ chưa lên Nitro",
                        ephemeral=True
                    )
                    return
                
                embed_msg = discord.Embed(
                    title=f"Avatar local của {member.display_name}",
                    color=discord.Color.random()
                )
                # use the guild‐avatar URL for both author icon and image
                embed_msg.set_author(
                    name=member.display_name,
                    icon_url=member.guild_avatar.url
                )
                embed_msg.set_image(url=member.guild_avatar.url)
                embed_msg.set_footer(
                    text=f"Bởi {interaction.user.display_name}",
                    icon_url=interaction.user.display_avatar.url
                )
                await interaction.response.send_message(embed=embed_msg)
        except Exception as e:
            await interaction.response.send_message(
                "Có lỗi xảy ra khi lấy avatar",
                ephemeral=True
            )
            print(f"Avatar command error: {e}")

    @app_commands.command(name='banner', description='lấy banner của bạn hoặc người khác (nếu bạn muốn khoe nitro)')
    async def banner(self, interaction: discord.Interaction, member: discord.Member = None):
        try:
            if member is None:
                member = interaction.user
            
            # Fetch the full user object to get banner data
            user = await self.bot.fetch_user(member.id)
            
            if user.banner is None:
                if user.accent_color:
                    embed_msg = discord.Embed(title=f"{user.display_name} không có banner",
                                description=f"Có mã màu banner: {user.accent_color}",
                                color=user.accent_color)
                    embed_msg.set_author(name=f"{user.display_name}",
                                icon_url=user.display_avatar.url)
                    embed_msg.set_footer(text=f"Bởi {interaction.user.display_name}",
                                icon_url=interaction.user.display_avatar.url)
                    await interaction.response.send_message(embed=embed_msg)
                else:
                    await interaction.response.send_message(f"{user.display_name} không có banner và không có mã màu banner")
            else:
                embed_msg = discord.Embed(title=f"Banner của {user.display_name}",
                                            color=discord.Color.random())
                embed_msg.set_author(name=f"{user.display_name}",
                                        icon_url=user.display_avatar.url)
                embed_msg.set_image(url=user.banner.url)
                embed_msg.set_footer(text=f"Bởi {interaction.user.display_name}",
                                        icon_url=interaction.user.display_avatar.url)
                await interaction.response.send_message(embed=embed_msg)
        except Exception as e:
            await interaction.response.send_message("Có lỗi xảy ra khi lấy banner", ephemeral=True)
            print(f"Banner command error: {e}")
