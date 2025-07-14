import discord
from discord.ext import commands
import os
from src import keep_alive
import asyncio
import random
from src.commands.command_manager import CommandManager
from src import constants
from src.error_handler import ErrorHandler
from src.config import Config
from src.database import MongoDatabase

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
        self.command_manager = CommandManager(self)
        
        # Initialize error handler
        self.error_handler = ErrorHandler(self.bot)
        
        # Initialize database handler
        self.database = MongoDatabase(collection_name="botdata")
        
        # Register event handlers
        self.register_events()
    
    def register_events(self):
        @self.bot.event
        async def on_ready():
            print(f'Logged in as {self.bot.user}')
            print(f'Bot version: {constants.BOT_VERSION}')

            # Sync slash commands
            try:
                synced = await self.bot.tree.sync()
                print(f"Synced {len(synced)} commands")
            except Exception as e:
                print(f"Failed to sync commands: {e}")
            
            if self.config.is_debug_mode():
                print('Running in debug mode')
                
            # Initialize MongoDB connection
            print("Connecting to MongoDB...")
            if self.database.load():
                print("Successfully connected to MongoDB!")
            else:
                print("Failed to connect to MongoDB - some features may not work")
        
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
        required_extensions = getattr(constants, 'REQUIRED_EXTENSIONS', {})
        for directory in constants.OTHER_EXTENSION_DIRECTORIES:
            # Correct the path for os.listdir
            corrected_directory = directory.replace('./', '')
            files = [f for f in os.listdir(corrected_directory) if f.endswith('.py')]
            category = directory.split('/')[-1]
            
            # Filter files if required extensions are specified
            if category in required_extensions:
                files = [f for f in files if f[:-3] in required_extensions[category]]
                
            random.shuffle(files)
            for filename in files:
                module_path = f'{directory.replace("./", "").replace("/", ".")}.{filename[:-3]}'
                await self.bot.load_extension(module_path)
                print(f"Loaded extension: {module_path}")
    
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


# Run the bot
if __name__ == '__main__':
    asyncio.run(main())