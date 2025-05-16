import discord
from discord.ext import commands
import os
import keep_alive
import asyncio
from dotenv import load_dotenv, find_dotenv
import random
from commands.command_manager import CommandManager
import constants


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
        
        # Register event handlers
        self.register_events()
        
    def register_events(self):
        @self.bot.event
        async def on_ready():
            print(f'Logged in as {self.bot.user}')
            print(f'Bot version: {constants.BOT_VERSION}')
        
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
            debug=False
        )
        
        # Load extensions
        await self.load_extensions()
        
        # Start the bot
        load_dotenv(find_dotenv())
        discord_token = os.getenv("discord_token")
        await self.bot.start(discord_token)


async def main():
    bot = DiscordBot()
    await bot.start()


if __name__ == "__main__":
    asyncio.run(main())