import discord
from discord.ext import commands
from discord import app_commands
from commands.base_command import GeneralCommand


class CommandInfoHandler:
    """Handler for command information and categories."""
    
    def __init__(self):
        # Định nghĩa trực tiếp các categories và commands thay vì đọc từ file
        self.categories = {
            "1": {
                "name": "General commands", 
                "description": "Các lệnh chung", 
                "commands": {
                    "avatar": "Xem avatar của người dùng",
                    "help": "Hiển thị menu trợ giúp",
                    "info": "Xem thông tin bot",
                    "banner": "Xem banner của người dùng",
                    "ping": "Kiểm tra độ trễ của bot"
                }
            },
            "2": {
                "name": "Fun commands", 
                "description": "Các lệnh giải trí", 
                "commands": {
                    "codejoke": "Xem joke về lập trình",
                    "dice": "Tung xúc xắc",
                    "fakemsg": "Tạo tin nhắn giả",
                    "im": "Lệnh im",
                    "mp5_leg": "Lệnh mp5_leg",
                    "phenis": "Lệnh phenis"
                }
            },
            "3": {
                "name": "Unclassified commands", 
                "description": "Lệnh này không biết phân loại ra sao", 
                "commands": {
                    "search": "Tìm kiếm trên Google",
                    "aiask": "Hỏi AI assistant"
                }
            }
        }
    
    def get_all_commands(self):
        """Get all commands from all categories."""
        all_commands = {}
        for category in self.categories.values():
            all_commands.update(category["commands"])
        return all_commands
    
    def get_category(self, category_id):
        """Get a specific category by ID."""
        return self.categories.get(category_id)
    
    def get_command_info(self, command_name):
        """Get information about a specific command."""
        all_commands = self.get_all_commands()
        return all_commands.get(command_name.lower())
    
    def add_command(self, category_id, command_name, command_description):
        """Add a new command to a category."""
        if category_id in self.categories:
            self.categories[category_id]["commands"][command_name.lower()] = command_description
            return True
        return False


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
