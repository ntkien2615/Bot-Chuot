"""
Help system views and UI components
"""
import discord
from src import constants


class HelpDropdown(discord.ui.Select):
    """Dropdown menu để chọn category lệnh"""
    
    def __init__(self, command_manager):
        self.command_manager = command_manager
        
        # Tạo options cho dropdown
        options = [
            discord.SelectOption(
                label="🎮 Fun Commands", 
                value="fun", 
                description="Các lệnh giải trí và vui nhộn",
                emoji="🎮"
            ),
            discord.SelectOption(
                label="⚙️ General Commands", 
                value="general", 
                description="Các lệnh chung và tiện ích",
                emoji="⚙️"
            ),
            discord.SelectOption(
                label="🎲 Game Commands", 
                value="games", 
                description="Các trò chơi tương tác",
                emoji="🎲"
            ),
            discord.SelectOption(
                label="💰 Economy Commands", 
                value="economy", 
                description="Hệ thống kinh tế và tiền tệ",
                emoji="💰"
            )
        ]
        
        super().__init__(
            placeholder="🔍 Chọn loại lệnh để xem chi tiết...", 
            max_values=1, 
            min_values=1, 
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        """Xử lý khi user chọn category"""
        category = self.values[0]
        
        # Lấy commands từ category
        commands = self.command_manager.get_commands_by_category(category)
        
        if not commands:
            embed = discord.Embed(
                title="❌ Không tìm thấy lệnh",
                description=f"Không có lệnh nào trong mục **{category}**",
                color=discord.Color.red()
            )
            await interaction.response.edit_message(embed=embed, view=self.view)
            return
        
        # Tạo embed cho category
        category_name = constants.CATEGORY_NAMES.get(category, category.title())
        embed = self.create_category_embed(category, category_name, commands)
        
        await interaction.response.edit_message(embed=embed, view=self.view)
    
    def create_category_embed(self, category: str, category_name: str, commands) -> discord.Embed:
        """Tạo embed hiển thị commands trong category"""
        
        # Màu sắc theo category
        colors = {
            "fun": discord.Color.orange(),
            "general": discord.Color.blue(), 
            "games": discord.Color.green(),
            "economy": discord.Color.gold()
        }
        
        # Emoji cho category
        emojis = {
            "fun": "🎮",
            "general": "⚙️",
            "games": "🎲", 
            "economy": "💰"
        }
        
        color = colors.get(category, discord.Color.random())
        emoji = emojis.get(category, "📋")
        
        embed = discord.Embed(
            title=f"{emoji} {category_name}",
            description=f"📝 **Tổng cộng: {len(commands)} lệnh**\n"
                       f"💡 Sử dụng `/tên_lệnh` để thực thi",
            color=color
        )
        
        # Thêm commands vào embed
        for i, cmd in enumerate(commands, 1):
            name = getattr(cmd, 'name', 'Không tên')
            desc = getattr(cmd, 'description', 'Không có mô tả')
            
            # Thêm số thứ tự và format đẹp
            embed.add_field(
                name=f"{i}. `/{name}`",
                value=f"📄 {desc}",
                inline=False
            )
        
        # Footer với thông tin thêm
        embed.set_footer(
            text=f"💡 Tip: Gõ / và tên lệnh để xem thêm chi tiết • Category: {category}",
            icon_url="https://cdn.discordapp.com/emojis/💡.png"
        )
        
        return embed


class HelpDropdownView(discord.ui.View):
    """View chứa dropdown menu"""
    
    def __init__(self, command_manager):
        super().__init__(timeout=300)  # 5 phút timeout
        self.command_manager = command_manager
        self.add_item(HelpDropdown(command_manager))
    
    async def on_timeout(self):
        """Xử lý khi view timeout"""
        # Disable tất cả components
        for item in self.children:
            if isinstance(item, (discord.ui.Button, discord.ui.Select)):
                item.disabled = True


class InfoButton(discord.ui.Button):
    """Button hiển thị thông tin bot"""
    
    def __init__(self):
        super().__init__(
            label="ℹ️ Thông tin Bot",
            style=discord.ButtonStyle.secondary,
            emoji="ℹ️"
        )
    
    async def callback(self, interaction: discord.Interaction):
        """Hiển thị thông tin về bot"""
        embed = discord.Embed(
            title="🤖 Thông tin Bot",
            description="Bot được phát triển với Discord.py",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="📊 Thống kê",
            value="🔧 Đang phát triển\n"
                  "🎮 Nhiều tính năng\n"
                  "⚡ Hiệu suất cao",
            inline=True
        )
        
        embed.add_field(
            name="🔗 Liên kết",
            value="📖 [Hướng dẫn](https://example.com)\n"
                  "🐛 [Báo lỗi](https://example.com)\n"
                  "💝 [Hỗ trợ](https://example.com)",
            inline=True
        )
        
        embed.set_footer(text="Cảm ơn bạn đã sử dụng bot!")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)


class HelpMainView(discord.ui.View):
    """View chính cho help command với buttons và dropdown"""
    
    def __init__(self, command_manager):
        super().__init__(timeout=300)
        self.command_manager = command_manager
        
        # Thêm dropdown
        self.add_item(HelpDropdown(command_manager))
        
        # Thêm info button
        self.add_item(InfoButton())
    
    async def on_timeout(self):
        """Xử lý khi view timeout"""
        for item in self.children:
            if isinstance(item, (discord.ui.Button, discord.ui.Select)):
                item.disabled = True
