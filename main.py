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
            # Basic startup info
            print(f'🤖 {self.bot.user} is online!')
            print(f'📊 Serving {len(self.bot.guilds)} guilds')

            # Sync slash commands
            try:
                synced = await self.bot.tree.sync()
                print(f"✅ Synced {len(synced)} commands")
            except Exception as e:
                print(f"❌ Command sync failed: {e}")
            
            # MongoDB connection (only show result)
            if self.database.load():
                print("✅ MongoDB connected")
            else:
                print("❌ MongoDB connection failed")
                
            # Debug mode indicator (minimal)
            if self.config.is_debug_mode():
                print('🐛 Debug mode: ON')
            else:
                print('🚀 Production mode: ON')
        
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
    
    async def run_bot(self):
        """Start the Discord bot with minimal logging"""
        # Get Discord token
        discord_token = self.config.get_token()
        if not discord_token:
            raise ValueError("❌ Discord token is not set in environment variables")
        
        # Start keep-alive service if URL provided
        keepalive_url = self.config.get_keepalive_url()
        if keepalive_url:
            keep_alive.awake(keepalive_url, debug=self.config.is_debug_mode())
            print(f"🔄 Keep-alive: {keepalive_url}")
        
        print("🚀 Starting bot...")
        await self.bot.start(discord_token)


async def main():
    """Main entry point"""
    bot = DiscordBot()
    await bot.run_bot()


# Run the bot
if __name__ == '__main__':
    asyncio.run(main())