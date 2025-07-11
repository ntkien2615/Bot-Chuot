import discord
from discord.ext import commands
from discord import app_commands
from commands.base_command import GeneralCommand


class BannerCommand(GeneralCommand):
    """Command to get user banners."""
    
    def __init__(self, bot):
        super().__init__(bot)
        self.name = "banner"
        self.description = "Lấy banner của bạn hoặc người khác"

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
