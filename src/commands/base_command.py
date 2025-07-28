import discord
from discord.ext import commands
from discord import app_commands


class BaseCommand(commands.Cog):
    """Base class for all commands to inherit from."""
    
    def __init__(self, discord_bot):
        self.discord_bot = discord_bot
        self.bot = discord_bot.bot
        self.config = discord_bot.config  # Add config access


class SlashCommand(BaseCommand):
    """Base class for slash commands."""
    
    pass


class PrefixCommand(BaseCommand):
    """Base class for prefix commands."""
    
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


class GameCommand(SlashCommand):
    """Base class for game commands that use slash commands."""
    
    category = "game"
    
    def __init__(self, bot):
        super().__init__(bot) 