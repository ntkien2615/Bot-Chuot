"""
PvP Command
Main command handler for PvP battles
"""

import discord
from discord import app_commands
from src.commands.base_command import GameCommand
from .views import ChallengeView
from .constants import EmbedColors, Emojis, GameConstants


class Pvp(GameCommand):
    """PvP command for Discord bot"""

    def __init__(self, discord_bot):
        super().__init__(discord_bot)

    @app_commands.command(name='pvp', description='Chơi pvp với người khác')
    @app_commands.describe(opponent='Người chơi bạn muốn thách đấu')
    async def pvp(self, interaction: discord.Interaction, opponent: discord.User):
        """Main PvP command"""
        
        # Validation checks
        if opponent == interaction.user:
            await interaction.response.send_message('❌ Bạn không thể tự thách đấu bản thân!', ephemeral=True)
            return
        
        if opponent.bot:
            await interaction.response.send_message('❌ Không thể thách đấu bot!', ephemeral=True)
            return
        
        # Create challenge embed
        embed = discord.Embed(
            title=f"{Emojis.CHALLENGE} LỜI THÁCH ĐẤU PVP",
            description=f"**{interaction.user.display_name}** đã gửi lời thách đấu đến bạn!\n\n🤔 Bạn có đồng ý không?",
            color=EmbedColors.CHALLENGE
        )
        embed.add_field(
            name=f"{Emojis.TIMEOUT} Thời gian:",
            value=f"{GameConstants.CHALLENGE_TIMEOUT} giây để quyết định",
            inline=False
        )
        embed.set_footer(text="Chọn phản ứng để tiếp tục...")
        
        # Create challenge view
        view = ChallengeView(interaction.user, opponent)
        view._interaction = interaction
        
        await interaction.response.send_message(f"{opponent.mention}", embed=embed, view=view)
