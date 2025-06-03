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
            
            member = await self.bot.fetch_user(member.id)
            
            if member.banner is None:
                if member.accent_color:
                    embed_msg = discord.Embed(title=f"{member} không có banner",
                                description=f"Có mã màu banner: {member.accent_color}",
                                color=member.accent_color)
                    embed_msg.set_author(name=f"{member}",
                                icon_url=member.avatar)
                    embed_msg.set_footer(text=f"Bởi {interaction.user}",
                                icon_url=interaction.user.avatar)
                    await interaction.response.send_message(embed=embed_msg)
                else:
                    await interaction.response.send_message(f"{member} không có banner và không có mã màu banner")
            else:
                embed_msg = discord.Embed(title=f"Banner của {member}",
                                            color=discord.Color.random())
                embed_msg.set_author(name=f"{member}",
                                        icon_url=member.avatar)
                embed_msg.set_image(url=member.banner.url)
                embed_msg.set_footer(text=f"Bởi {interaction.user}",
                                        icon_url=interaction.user.avatar)
                await interaction.response.send_message(embed=embed_msg)
        except Exception as e:
            await interaction.response.send_message("Có lỗi xảy ra khi lấy banner", ephemeral=True)
            print(f"Banner command error: {e}")


async def setup(bot):
    await bot.add_cog(BannerCommand(bot))
