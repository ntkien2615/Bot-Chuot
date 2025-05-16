import discord
from discord.ext import commands
from discord import app_commands
from abc import abstractmethod


class BaseCommand(commands.Cog):
    """Base class for all commands to inherit from."""
    
    def __init__(self, bot):
        self.bot = bot
        
    @abstractmethod
    async def execute(self, *args, **kwargs):
        """The main execution method that all command subclasses must implement."""
        pass


class SlashCommand(BaseCommand):
    """Base class for slash commands."""
    
    @abstractmethod
    async def register_slash_command(self):
        """Register the slash command."""
        pass


class PrefixCommand(BaseCommand):
    """Base class for prefix commands."""
    
    @abstractmethod
    async def register_prefix_command(self):
        """Register the prefix command."""
        pass


class FunCommand(SlashCommand):
    """Base class for fun commands that use slash commands."""
    
    category = "fun"
    
    def __init__(self, bot):
        super().__init__(bot)


class GeneralCommand(SlashCommand):
    """Base class for general commands that use slash commands."""
    
    category = "general"
    
    def __init__(self, bot):
        super().__init__(bot)


class UtilityCommand(SlashCommand):
    """Base class for utility commands that use slash commands."""
    
    category = "utility"
    
    def __init__(self, bot):
        super().__init__(bot) 