import os
import random
import importlib
import inspect
from commands.base_command import BaseCommand
import constants


class CommandManager:
    """Class responsible for loading and managing all commands."""
    
    def __init__(self, bot):
        self.bot = bot
        self.commands = []
        self.command_directories = constants.COMMAND_DIRECTORIES
        self.required_commands = constants.REQUIRED_COMMANDS
        
    async def load_all_commands(self):
        """Load all commands from the command directories."""
        for directory in self.command_directories:
            await self._load_commands_from_directory(directory)
    
    async def _load_commands_from_directory(self, directory):
        """Load all command modules from a specific directory."""
        try:
            # Get all Python files in the directory
            files = [f for f in os.listdir(directory) if f.endswith('.py')]
            
            # Filter files to only include required commands if specified
            category = directory.split('/')[-1]
            if category in self.required_commands:
                required_files = self.required_commands[category]
                files = [f for f in files if f[:-3] in required_files]
            
            # Randomize load order for variety
            random.shuffle(files)
            
            for filename in files:
                module_path = f'{directory.replace("./", "").replace("/", ".")}.{filename[:-3]}'
                await self.bot.load_extension(module_path)
                print(f"Loaded extension: {module_path}")
                
        except Exception as e:
            print(f"Failed to load commands from {directory}: {e}")
    
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