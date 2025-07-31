"""
Help command implementation
"""
import discord
from discord import app_commands
from src.commands.base_command import GeneralCommand
from .help_views import HelpMainView


class HelpCommand(GeneralCommand):
    """Command hiển thị menu trợ giúp"""
    
    def __init__(self, discord_bot):
        super().__init__(discord_bot)
        self.bot = discord_bot.bot
        # Lấy command_manager từ bot
        self.command_manager = getattr(discord_bot, 'command_manager', None)

    @app_commands.command(
        name="help", 
        description="📋 Hiển thị menu trợ giúp các lệnh của bot"
    )
    async def help_menu(self, interaction: discord.Interaction):
        """Hiển thị help menu với dropdown và buttons"""
        
        if not self.command_manager:
            embed = discord.Embed(
                title="❌ Lỗi hệ thống",
                description="Không thể lấy danh sách lệnh. Vui lòng thử lại sau.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        # Tạo embed chính
        embed = self.create_main_embed(interaction.user)
        
        # Tạo view với dropdown và buttons
        view = HelpMainView(self.command_manager)
        
        await interaction.response.send_message(embed=embed, view=view)
    
    def create_main_embed(self, user) -> discord.Embed:
        """Tạo embed chính cho help menu"""
        
        embed = discord.Embed(
            title="📋 Menu Trợ Giúp",
            description="🎯 **Chào mừng bạn đến với hệ thống trợ giúp!**\n"
                       "📝 Chọn loại lệnh bên dưới để xem danh sách chi tiết.",
            color=discord.Color.blue()
        )
        
        # Thêm thông tin hướng dẫn
        embed.add_field(
            name="🎮 Các loại lệnh có sẵn",
            value="🎭 **Fun Commands** - Lệnh giải trí\n"
                  "⚙️ **General Commands** - Lệnh chung\n"
                  "🎲 **Game Commands** - Trò chơi\n"
                  "💰 **Economy Commands** - Hệ thống kinh tế",
            inline=False
        )
        
        embed.add_field(
            name="💡 Cách sử dụng",
            value="1️⃣ Chọn loại lệnh từ menu dropdown\n"
                  "2️⃣ Xem danh sách lệnh chi tiết\n" 
                  "3️⃣ Gõ `/tên_lệnh` để sử dụng\n"
                  "4️⃣ Bấm nút ℹ️ để xem thông tin bot",
            inline=False
        )
        
        embed.add_field(
            name="⚡ Lưu ý",
            value="• Menu sẽ tự động hết hạn sau 5 phút\n"
                  "• Một số lệnh cần quyền đặc biệt\n"
                  "• Sử dụng lệnh một cách có trách nhiệm",
            inline=False
        )
        
        embed.set_footer(
            text=f"Được yêu cầu bởi {user.display_name} • Bot phiên bản 2.0",
            icon_url=user.display_avatar.url
        )
        
        embed.set_thumbnail(url=self.bot.user.display_avatar.url if self.bot.user else None)
        
        return embed
