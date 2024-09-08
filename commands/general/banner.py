import discord
from discord.ext import commands
from discord import app_commands


class Banner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='banner', description='lấy banner của bạn hoặc người khác (nếu bạn muốn khoe nitro)')
    async def bannerslash(self, interaction: discord.Interaction, member: discord.Member = None):
        if member == None:
            member = interaction.user
        
        member = await self.bot.fetch_user(member.id)
        if member.banner is None:
            await interaction.response.send_message(embed=discord.Embed(
                description="this user has no banner."
            ))
        else:
            embed_msg = discord.Embed(title=f"Banner global của {member}",
                                        color=discord.Color.random())
            embed_msg.set_author(name=f"{member}",
                                    icon_url=member.avatar)
            embed_msg.set_image(url=member.banner.url)
            embed_msg.set_footer(text=f"Bởi {interaction.user}",
                                    icon_url=interaction.user.avatar)
            await interaction.response.send_message(embed=embed_msg)
    

async def setup(bot):
    await bot.add_cog(Banner(bot))
