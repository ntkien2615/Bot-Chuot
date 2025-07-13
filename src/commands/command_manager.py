import os
import random
import importlib
import inspect
from src.commands.base_command import BaseCommand, SlashCommand, PrefixCommand, FunCommand, GeneralCommand
from src import constants


class CommandManager:
    """Class responsible for loading and managing all commands."""
    
    def __init__(self, discord_bot):
        self.discord_bot = discord_bot
        self.bot = discord_bot.bot
        self.commands = []
        self.command_directories = constants.COMMAND_DIRECTORIES
        
    async def load_all_commands(self):
        """Load all commands from the command directories."""
        for directory in self.command_directories:
            await self._load_commands_from_directory(directory)
    
    async def _load_commands_from_directory(self, directory):
        """Load all command modules from a specific directory and register commands."""
        for root, _, files in os.walk(directory):
            for filename in files:
                if filename.endswith('.py') and not filename.startswith('__'):
                    # Construct the module path correctly
                    module_path = os.path.join(root, filename) \
                        .replace(os.sep, '.') \
                        .replace('.py', '')

                    try:
                        # Import the module
                        module = importlib.import_module(module_path)
                        
                        # Find command classes within the module
                        for name, obj in inspect.getmembers(module):
                            # Check if it's a class, a subclass of BaseCommand, and not one of the base classes themselves
                            if inspect.isclass(obj) and issubclass(obj, BaseCommand) and obj not in [BaseCommand, SlashCommand, PrefixCommand, FunCommand, GeneralCommand]:
                                # Instantiate the command and add as cog
                                command_instance = obj(self.discord_bot)
                                await self.bot.add_cog(command_instance)
                                self.register_command(command_instance) # Register with CommandManager
                                # print(f"Loaded and registered command: {module_path}.{name}")
                                break # Assuming one main command class per file
                    except Exception as e:
                        print(f"Failed to load and register command from {module_path}: {e}")
    
    def register_command(self, command):
        """Register a command instance."""
        if isinstance(command, BaseCommand):
            self.commands.append(command)
            return True
        return False
    
    def get_commands_by_category(self, category):
        """Get all commands belonging to a specific category."""
        return [cmd for cmd in self.commands if hasattr(cmd, 'category') and cmd.category == category]
    
    def get_command_by_name(self, name):
        """Get a command by its name."""
        for command in self.commands:
            command_name = getattr(command, 'name', None)
            if command_name and command_name.lower() == name.lower():
                return command
        return None 

    def get_all_categories(self):
        """Return a dict of {category_id: category_name} for all loaded commands."""
        categories = {}
        for cmd in self.commands:
            if hasattr(cmd, 'category'):
                cat_id = cmd.category
                cat_name = constants.CATEGORY_NAMES.get(cat_id, cat_id)
                categories[cat_id] = cat_name
        return categories 