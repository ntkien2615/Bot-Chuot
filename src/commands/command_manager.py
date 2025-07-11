import os
import random
import importlib
import inspect
from src.commands.base_command import BaseCommand, SlashCommand, PrefixCommand, FunCommand, GeneralCommand, UtilityCommand
from src import constants


class CommandManager:
    """Class responsible for loading and managing all commands."""
    
    def __init__(self, bot):
        self.bot = bot
        self.commands = []
        self.command_directories = constants.COMMAND_DIRECTORIES
        
    async def load_all_commands(self):
        """Load all commands from the command directories."""
        for directory in self.command_directories:
            await self._load_commands_from_directory(directory)
    
    async def _load_commands_from_directory(self, directory):
        """Load all command modules from a specific directory and register commands."""
        try:
            # Correct the path for os.listdir
            corrected_directory = directory.replace('./', '')
            files = [f for f in os.listdir(corrected_directory) if f.endswith('.py') and not f.startswith('__')]

            for filename in files:
                module_name = filename[:-3]
                module_path = f'{corrected_directory.replace("/", ".")}.{module_name}'
                
                try:
                    # Import the module
                    module = importlib.import_module(module_path)
                    
                    # Find command classes within the module
                    for name, obj in inspect.getmembers(module):
                        # Check if it's a class, a subclass of BaseCommand, and not one of the base classes themselves
                        if inspect.isclass(obj) and issubclass(obj, BaseCommand) and obj not in [BaseCommand, SlashCommand, PrefixCommand, FunCommand, GeneralCommand, UtilityCommand]:
                            # Instantiate the command and add as cog
                            command_instance = obj(self.bot)
                            await self.bot.add_cog(command_instance)
                            self.register_command(command_instance) # Register with CommandManager
                            print(f"Loaded and registered command: {module_path}.{name}")
                            break # Assuming one main command class per file
                except Exception as e:
                    print(f"Failed to load and register command from {module_path}: {e}")
                
        except Exception as e:
            print(f"Failed to process directory {directory}: {e}")
    
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