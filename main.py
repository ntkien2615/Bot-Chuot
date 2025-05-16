import discord
from discord.ext import commands
import os
import keep_alive
import asyncio
import random
from commands.command_manager import CommandManager
import constants
from error_handler import ErrorHandler
from config import Config


class FileHandler:
    @staticmethod
    def random_file_read(file_path):
        try:
            with open(file_path, "r") as f:
                lines = f.readlines()
            if lines:
                return random.choice(lines).strip()
        except (IndexError, FileNotFoundError) as e:
            return None

    @staticmethod
    def file_read_with_line(file_path, line):
        try:
            with open(file_path, "r") as f:
                lines = f.readlines()
            if lines:
                return lines[line].strip()
        except (IndexError, FileNotFoundError) as e:
            return None


class DiscordBot:
    def __init__(self):
        # Load config
        self.config = Config()
        
        # Setup intents
        self.intents = discord.Intents.default()
        self.intents.typing = False
        self.intents.message_content = True
        self.intents.members = True
        
        # Initialize bot
        self.bot = commands.Bot(
            command_prefix=constants.BOT_PREFIX,
            intents=self.intents,
            help_command=None,
            case_insensitive=True,
            description=constants.BOT_DESCRIPTION
        )
        
        # Initialize command manager
        self.command_manager = CommandManager(self.bot)
        
        # Initialize file handler
        self.file_handler = FileHandler()
        
        # Initialize error handler
        self.error_handler = ErrorHandler(self.bot)
        
        # Register event handlers
        self.register_events()
        
    def register_events(self):
        @self.bot.event
        async def on_ready():
            print(f'Logged in as {self.bot.user}')
            print(f'Bot version: {constants.BOT_VERSION}')
            
            if self.config.is_debug_mode():
                print('Running in debug mode')
        
        @self.bot.event
        async def on_command_error(ctx, error):
            if isinstance(error, commands.CommandOnCooldown):
                await ctx.send(f'This command is on cooldown. Try again in {error.retry_after:.2f} seconds.')
            else:
                raise error
    
    async def load_extensions(self):
        # Load commands through command manager
        await self.command_manager.load_all_commands()
        
        # Load other extensions
        for directory in constants.OTHER_EXTENSION_DIRECTORIES:
            files = [f for f in os.listdir(directory) if f.endswith('.py')]
            random.shuffle(files)
            for filename in files:
                await self.bot.load_extension(f'{directory.replace("./", "").replace("/", ".")}.{filename[:-3]}')
    
    async def start(self):
        # Keep the bot alive
        keep_alive.awake(
            constants.KEEPALIVE_URL,
            debug=self.config.is_debug_mode()
        )
        
        # Load extensions
        await self.load_extensions()
        
        # Start the bot
        discord_token = self.config.get_token()
        if not discord_token:
            raise ValueError("Discord token is not set in environment variables")
            
        await self.bot.start(discord_token)


async def main():
    bot = DiscordBot()
    await bot.start()


if __name__ == "__main__":
    asyncio.run(main())