import discord
from discord import app_commands
from discord.ext import commands
from src.commands.base_command import GeneralCommand
from src.commands.command_manager import CommandManager
from src import constants

class HelpDropdown(discord.ui.Select):
    def __init__(self, command_manager):
        self.command_manager = command_manager
        options = [
            discord.SelectOption(label="Fun Commands", value="fun", description="Các lệnh giải trí"),
            discord.SelectOption(label="General Commands", value="general", description="Các lệnh chung")
        ]
        super().__init__(placeholder="Chọn loại lệnh để xem...", max_values=1, min_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        category = self.values[0]
        commands = self.command_manager.get_commands_by_category(category)
        if not commands:
            await interaction.response.edit_message(content=f"Không có lệnh nào trong mục {category}", embed=None, view=self.view)
            return
        embed = discord.Embed(title=f"Danh sách lệnh: {constants.CATEGORY_NAMES.get(category, category)}", color=discord.Color.random())
        for cmd in commands:
            name = getattr(cmd, 'name', 'Không tên')
            desc = getattr(cmd, 'description', 'Không có mô tả')
            embed.add_field(name=f"/{name}", value=desc, inline=False)
        await interaction.response.edit_message(embed=embed, view=self.view)

class HelpDropdownView(discord.ui.View):
    def __init__(self, command_manager):
        super().__init__()
        self.add_item(HelpDropdown(command_manager))

class HelpCommand(GeneralCommand):
    def __init__(self, discord_bot):
        super().__init__(discord_bot)
        self.bot = discord_bot.bot
        # Lấy command_manager từ bot (giả định đã gán vào bot)
        self.command_manager = getattr(discord_bot, 'command_manager', None)

    @app_commands.command(name="help", description="Hiển thị menu trợ giúp các lệnh của bot")
    async def help_menu(self, interaction: discord.Interaction):
        if not self.command_manager:
            await interaction.response.send_message("Không thể lấy danh sách lệnh.")
            return
        embed = discord.Embed(title="Help Menu", description="Chọn loại lệnh để xem danh sách.", color=discord.Color.random())
        view = HelpDropdownView(self.command_manager)
        await interaction.response.send_message(embed=embed, view=view)
