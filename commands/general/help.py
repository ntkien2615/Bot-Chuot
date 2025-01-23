import discord
from discord.ext import commands
from discord import app_commands
import json
import os

class Commands:
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

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.commands_handler = Commands()

    @app_commands.command(name='help', description='trợ giúp')
    async def menu(self, interaction: discord.Interaction):
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

async def setup(bot):
    await bot.add_cog(HelpCog(bot))
