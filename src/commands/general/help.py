import discord
from discord.ext import commands
from discord import app_commands
from src.commands.base_command import GeneralCommand
from src import constants


class SelectDropdown(discord.ui.Select):
    def __init__(self, command_manager):
        self.command_manager = command_manager
        
        # Create options from command manager categories
        options = []
        for category_id, category_name in self.command_manager.get_all_categories().items():
            options.append(discord.SelectOption(
                label=category_name,
                value=category_id,
                description=f"Commands in the {category_name} category"
            ))

        super().__init__(placeholder="Chọn một lựa chọn nào",
                         max_values=1, min_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        category_id = self.values[0]
        category_name = self.command_manager.get_all_categories()[category_id]
        commands_in_category = self.command_manager.get_commands_by_category(category_id)

        embed = discord.Embed(
            title=category_name,
            description="",
            color=discord.Color.random()
        )
        
        for cmd in commands_in_category:
            embed.add_field(name=f"/{cmd.name}", value=cmd.description, inline=False)
            
        embed.set_footer(text=f"Requested by {interaction.user}",
                        icon_url=interaction.user.avatar)
        await interaction.response.edit_message(embed=embed)


class DropdownMenu(discord.ui.View):
    def __init__(self, command_manager):
        super().__init__()
        self.add_item(SelectDropdown(command_manager))


class HelpCommand(GeneralCommand):
    """Command to display help menu with all available commands."""
    
    def __init__(self, bot):
        super().__init__(bot)
        self.name = "help"
        self.description = "Hiển thị trợ giúp về các lệnh"
    
    @app_commands.command(name='help', description='Hiển thị trợ giúp về các lệnh')
    async def help(self, interaction: discord.Interaction):
        """Execute the help command."""
        command_manager = self.discord_bot.command_manager
        view = DropdownMenu(command_manager)
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
