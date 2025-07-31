"""
Rock Paper Scissors Multiplayer Command
"""
import discord
from discord.ext import commands
from discord import app_commands

from src.commands.base_command import GameCommand
from .rps_views import InviteRPSView


class MultiplayerRPS(GameCommand):
    """Rock Paper Scissors multiplayer game"""
    
    def __init__(self, discord_bot):
        super().__init__(discord_bot)
    
    @app_commands.command(
        name='rps',
        description='Chơi kéo búa bao với nhiều người!'
    )
    @app_commands.describe(
        max_players='Số người chơi tối đa (2-8, mặc định 8)'
    )
    async def rps_multi(
        self,
        interaction: discord.Interaction,
        max_players: int = 8
    ):
        """Command chính để tạo game RPS multiplayer"""
        
        # Kiểm tra guild
        if not interaction.guild:
            await interaction.response.send_message(
                "❌ Lệnh này chỉ có thể sử dụng trong server!",
                ephemeral=True
            )
            return
        
        # Kiểm tra user là Member
        if not isinstance(interaction.user, discord.Member):
            await interaction.response.send_message(
                "❌ Lỗi: Không thể xác định thông tin người dùng!",
                ephemeral=True
            )
            return
        
        # Kiểm tra max_players
        if max_players < 2 or max_players > 8:
            await interaction.response.send_message(
                "❌ Số người chơi tối đa phải từ 2 đến 8!",
                ephemeral=True
            )
            return
        
        # Tạo embed mời chơi
        embed = discord.Embed(
            title="✂️ 🪨 📄 ROCK PAPER SCISSORS",
            description="🎯 **Game đối kháng nhiều người chơi!**\n"
                       "🔥 Mọi người sẽ chọn bí mật trong tin nhắn riêng\n"
                       "⚡ Ai có lựa chọn thông minh nhất sẽ thắng!",
            color=discord.Color.gold()
        )
        
        embed.add_field(
            name=f"👥 Người chơi (1/{max_players})",
            value=f"🎮 {interaction.user.mention}",
            inline=False
        )
        
        embed.add_field(
            name="� Luật chơi",
            value="🪨 **Búa** thắng **Kéo** ✂️\n"
                  "✂️ **Kéo** thắng **Bao** 📄\n" 
                  "📄 **Bao** thắng **Búa** 🪨",
            inline=True
        )
        
        embed.add_field(
            name="🎮 Hướng dẫn",
            value="• 🎯 Bấm **Tham gia** để vào game\n"
                  "• 🚀 Host bấm **Bắt đầu** khi đủ người\n"
                  "• ⏰ Có 30 giây để chọn bằng nút\n"
                  "• 🏆 Kết quả sẽ được công bố\n"
                  "• ⚠️ Game tự hủy sau 30s nếu không hoạt động",
            inline=True
        )
        
        embed.set_footer(
            text=f"🎭 Host: {interaction.user.display_name} | Cần ít nhất 2 người chơi",
            icon_url=interaction.user.display_avatar.url
        )
        
        # Tạo invite view
        invite_view = InviteRPSView(interaction.user, max_players)
        
        await interaction.response.send_message(embed=embed, view=invite_view)
        
        # Lưu message reference để xử lý timeout
        try:
            message = await interaction.original_response()
            invite_view.message = message
        except Exception:
            pass  # Ignore lỗi nếu không lấy được message
