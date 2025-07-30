import discord
from discord.ext import commands
import os
import time
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

            # Load extensions and sync commands after bot is ready
            print("📦 Loading extensions...")
            await self.load_extensions()

            # MongoDB connection (only show result)
            print("🗄️ Connecting to MongoDB...")
            if self.database.load():
                print("✅ MongoDB connected")
            else:
                print("❌ MongoDB connection failed")
                
            # Debug mode indicator (minimal)
            if self.config.is_debug_mode():
                print('🐛 Debug mode: ON')
            else:
                print('🚀 Production mode: ON')
                
            print("✅ Bot startup complete!")
        
        @self.bot.event
        async def on_command_error(ctx, error):
            if isinstance(error, commands.CommandOnCooldown):
                await ctx.send(f'This command is on cooldown. Try again in {error.retry_after:.2f} seconds.')
            else:
                raise error
                
        @self.bot.event
        async def on_connect():
            print("🔗 Discord connection established")
            
        @self.bot.event
        async def on_disconnect():
            print("⚠️ Discord connection lost")
            
        @self.bot.event
        async def on_resumed():
            print("🔄 Discord connection resumed")
    
    async def load_extensions(self):
        # Load commands through command manager
        await self.command_manager.load_all_commands()
        
        # Load other extensions
        required_extensions = getattr(constants, 'REQUIRED_EXTENSIONS', {})
        for directory in constants.OTHER_EXTENSION_DIRECTORIES:
            if os.path.exists(directory):
                files = [f for f in os.listdir(directory) if f.endswith('.py')]
                category = directory.split('/')[-1]
                
                # Filter files if required extensions are specified
                if category in required_extensions:
                    files = [f for f in files if f[:-3] in required_extensions[category]]
                    
                random.shuffle(files)
                for filename in files:
                    module_path = f'{directory.replace("/", ".")}.{filename[:-3]}'
                    try:
                        await self.bot.load_extension(module_path)
                        print(f"Loaded extension: {module_path}")
                    except Exception as e:
                        print(f"Failed to load extension {module_path}: {e}")
        
        # Sync slash commands after loading all (with rate limit protection)
        try:
            # Check last sync time to avoid rate limiting
            last_sync_file = ".last_sync"
            should_sync = True
            
            if os.path.exists(last_sync_file):
                try:
                    with open(last_sync_file, 'r') as f:
                        last_sync_time = float(f.read().strip())
                    # Only sync if last sync was more than 5 minutes ago
                    if time.time() - last_sync_time < 300:  # 5 minutes
                        should_sync = False
                        print(f"⏰ Skipping sync - last sync was recent")
                except:
                    pass
            
            if should_sync:
                # Check if commands need syncing by comparing counts
                current_commands = await self.bot.tree.fetch_commands()
                loaded_commands = len([cmd for cmd in self.bot.tree.walk_commands()])
                
                if len(current_commands) != loaded_commands:
                    synced = await self.bot.tree.sync()
                    print(f"✅ Synced {len(synced)} slash commands")
                    
                    # Save sync time
                    with open(last_sync_file, 'w') as f:
                        f.write(str(time.time()))
                else:
                    print(f"✅ Commands already synced ({len(current_commands)} commands)")
            else:
                loaded_commands = len([cmd for cmd in self.bot.tree.walk_commands()])
                print(f"✅ Using cached commands ({loaded_commands} commands)")
                
        except discord.HTTPException as e:
            if e.status == 429:
                print(f"⚠️ Rate limited - commands will sync automatically later")
            else:
                print(f"❌ Command sync failed: {e}")
        except Exception as e:
            print(f"❌ Command sync failed: {e}")
    
    async def run_bot(self):
        """Start the Discord bot with minimal logging"""
        # Get Discord token
        discord_token = self.config.get_token()
        if not discord_token:
            raise ValueError("❌ Discord token is not set in environment variables")
        
        # Validate token format (basic check)
        if not discord_token.startswith(('MTA', 'MT', 'NTA', 'NT', 'OD')):
            print("⚠️ Warning: Discord token format looks suspicious")
        else:
            print("✅ Discord token format validated")
        
        # Start keep-alive service if URL provided
        keepalive_url = self.config.get_keepalive_url()
        if keepalive_url:
            keep_alive.awake(keepalive_url, debug=self.config.is_debug_mode())
            print(f"🔄 Keep-alive: {keepalive_url}")
        
        print("🚀 Starting bot...")
        print("🔗 Attempting Discord connection...")
        
        try:
            await self.bot.start(discord_token)
        except discord.LoginFailure:
            print("❌ Discord login failed - invalid token")
            raise
        except Exception as e:
            print(f"❌ Failed to start bot: {e}")
            raise


async def main():
    """Main entry point"""
    bot = DiscordBot()
    await bot.run_bot()


# Run the bot
if __name__ == '__main__':
    asyncio.run(main())