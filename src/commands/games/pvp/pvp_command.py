"""
PvP Command
Main command handler for PvP battles
"""

import discord
from discord import app_commands
from typing import Optional
from src.commands.base_command import GameCommand
from .views import ChallengeView
from .constants import EmbedColors, Emojis, GameConstants


class Pvp(GameCommand):
    """PvP command for Discord bot"""

    def __init__(self, discord_bot):
        super().__init__(discord_bot)

    @app_commands.command(name='pvp', description='Chơi pvp với người khác hoặc xem hướng dẫn')
    @app_commands.describe(opponent='Người chơi bạn muốn thách đấu (để trống để xem hướng dẫn)')
    async def pvp(self, interaction: discord.Interaction, opponent: Optional[discord.User] = None):
        """Main PvP command"""
        
        # Nếu không có đối thủ, hiển thị hướng dẫn
        if opponent is None:
            await self.show_guide(interaction)
            return
        
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
            description=f"**{interaction.user.display_name}** thách đấu **{opponent.display_name}**!\n\n🤔 Bạn có đồng ý không?",
            color=EmbedColors.CHALLENGE
        )
        embed.add_field(
            name=f"{Emojis.TIMEOUT} Thời gian:",
            value=f"{GameConstants.CHALLENGE_TIMEOUT}s để quyết định",
            inline=True
        )
        embed.set_footer(text="Nhấn nút để phản hồi...")
        
        # Create challenge view
        view = ChallengeView(interaction.user, opponent)
        view._interaction = interaction
        
        await interaction.response.send_message(f"{opponent.mention}", embed=embed, view=view)

    async def show_guide(self, interaction: discord.Interaction):
        """Hiển thị hướng dẫn chơi PvP"""
        embed = discord.Embed(
            title=f"{Emojis.CHALLENGE} HƯỚNG DẪN GAME PVP",
            description="**Game đấu 1v1 turn-based với hệ thống combat đa dạng!**",
            color=EmbedColors.CHALLENGE
        )
        
        # Cách chơi
        embed.add_field(
            name="🎮 Cách chơi:",
            value=f"• Sử dụng `/pvp @người_chơi` để thách đấu\n• Mỗi người có **{GameConstants.MAX_HP} HP** và **{GameConstants.MAX_ENERGY} Energy**\n• Lượt chơi xen kẽ, thắng khi đối thủ hết HP",
            inline=False
        )
        
        # Các hành động
        actions_text = f"""
{Emojis.PUNCH} **Đấm** ({GameConstants.PUNCH_ENERGY} energy): Sát thương vật lý cơ bản
{Emojis.MAGIC} **Phép thuật** ({GameConstants.MAGIC_ENERGY_BASE}-{GameConstants.MAGIC_ENERGY_DEVASTATE} energy): Sát thương phép, bỏ qua giáp vật lý
{Emojis.ARMOR} **Giáp vật lý** ({GameConstants.ARMOR_ENERGY} energy): Giảm sát thương vật lý
{Emojis.MAGIC_ARMOR} **Giáp phép** ({GameConstants.MAGIC_ARMOR_ENERGY} energy): Giảm sát thương phép
{Emojis.HEAL} **Hồi máu** ({GameConstants.HEAL_ENERGY} energy): Khôi phục HP
{Emojis.REST} **Nghỉ ngơi** (0 energy): Hồi {GameConstants.REST_ENERGY} energy
{Emojis.RUN} **Chạy trốn** (0 energy): Đầu hàng và kết thúc game
        """
        embed.add_field(
            name="⚔️ Các hành động:",
            value=actions_text,
            inline=False
        )
        
        # Hệ thống đặc biệt
        special_text = f"""
• **Chí mạng** ({GameConstants.CRIT_CHANCE}%): Gây thêm sát thương
• **True Damage** ({GameConstants.TRUE_DAMAGE_CHANCE}%): Bỏ qua mọi giáp
• **Energy tự hồi** {GameConstants.ENERGY_REGEN}/lượt
• **AFK timeout**: {GameConstants.AFK_TIMEOUT}s (tự động thua)
        """
        embed.add_field(
            name="✨ Hệ thống đặc biệt:",
            value=special_text,
            inline=False
        )
        
        embed.set_footer(text="Sử dụng /pvp @tên_người để bắt đầu thách đấu!")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
