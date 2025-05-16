import discord
from discord.ext import commands
from discord import app_commands
import json
import os
from commands.base_command import GeneralCommand

class CommandInfoHandler:
    def __init__(self):
        self.categories = {
            "1": {"name": "General commands", "description": "Các lệnh chung", "commands": {}},
            "2": {"name": "Fun commands", "description": "Các lệnh giải trí", "commands": {}},
            "3": {"name": "Unclassified commands", "description": "Lệnh này không biết phân loại ra sao", "commands": {}}
        }
        self.load_commands()
    
    def load_commands(self):
        commands_dir = "./commands_info"
        for category_id in self.categories:
            file_path = os.path.join(commands_dir, f"category_{category_id}.json")
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.categories[category_id]["commands"] = json.load(f)

class SelectDropdown(discord.ui.Select):
    def __init__(self, commands_handler):
        self.commands_handler = commands_handler
        options = [
            discord.SelectOption(
                label=cat["name"], 
                value=cat_id,
                description=cat["description"]
            ) for cat_id, cat in commands_handler.categories.items()
        ]
        super().__init__(placeholder="Chọn một lựa chọn nào",
                         max_values=1, min_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        category = self.commands_handler.categories[self.values[0]]
        embed = discord.Embed(
            title=category["name"],
            description="",
            color=discord.Color.random()
        )
        
        for cmd_name, cmd_desc in category["commands"].items():
            embed.add_field(name=f"/{cmd_name}", value=cmd_desc, inline=False)
            
        embed.set_footer(text=f"Requested by {interaction.user}",
                        icon_url=interaction.user.avatar)
        await interaction.response.edit_message(embed=embed)

class DropdownMenu(discord.ui.View):
    def __init__(self, commands_handler):
        super().__init__()
        self.add_item(SelectDropdown(commands_handler))

class HelpCommand(GeneralCommand):
    """Command to display help menu with all available commands."""
    
    def __init__(self, bot):
        super().__init__(bot)
        self.name = "help"
        self.description = "Hiển thị trợ giúp về các lệnh"
        self.commands_handler = CommandInfoHandler()
    
    async def register_slash_command(self):
        """Register the help slash command."""
        pass  # Handled by Discord.py's decorator system
    
    async def execute(self, interaction):
        """Execute the help command."""
        view = DropdownMenu(self.commands_handler)
        embed_msg = discord.Embed(
            title="HELP COMMAND",
            description="Dưới đây là các lệnh hiện tại của Chuột, sau này admin sẽ cập nhật thêm",
            color=discord.Color.random()
        )
        embed_msg.set_thumbnail(
            url='https://images-ext-1.discordapp.net/external/4l1sSRH8ZyOAWjLY9KyMefCCwzKQqbQdZp5-FHo3pKg/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/104272908108.png?format=webp&quality=lossless&width=676&height=676')
        embed_msg.set_footer(text=f"Requested by {interaction.user}",
                             icon_url=interaction.user.avatar)

        await interaction.response.send_message(
            embed=embed_msg, view=view)
    
    @app_commands.command(name='help', description='Hiển thị trợ giúp về các lệnh')
    async def help(self, interaction: discord.Interaction):
        await self.execute(interaction)

async def setup(bot):
    await bot.add_cog(HelpCommand(bot))
