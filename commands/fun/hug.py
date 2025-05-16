import discord
from discord.ext import commands
from discord import app_commands
from commands.base_command import FunCommand


class HugCommand(FunCommand):
    """Command to hug another user."""
    
    def __init__(self, bot):
        super().__init__(bot)
        self.name = "hug"
        self.description = "Ôm homie của bạn"
        self.hug_image_url = "https://media.discordapp.net/attachments/1077255654512787537/1346371351128051712/images.png?ex=67c7f188&is=67c6a008&hm=89e6adae2479be8138071a3a6fdf9c312daeb6297e5062c9c3a03830782d3135&=&format=webp&quality=lossless&width=376&height=210"
    
    async def register_slash_command(self):
        """Register the hug slash command."""
        pass  # This is handled by Discord.py's decorator system
    
    async def execute(self, interaction, user):
        """Execute the hug command."""
        target_user = user or interaction.user
        
        embed = discord.Embed(
            title="", 
            description=f'{interaction.user} đã ôm {target_user.mention}, thật ngọt ngào!!!', 
            color=discord.Color.random()
        )
        embed.set_image(url=self.hug_image_url)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name='hug', description='Ôm homie của bạn')
    @app_commands.describe(user='Người bạn muốn ôm')
    async def hug(self, interaction: discord.Interaction, user: discord.Member):
        await self.execute(interaction, user)


async def setup(bot):
    await bot.add_cog(HugCommand(bot))