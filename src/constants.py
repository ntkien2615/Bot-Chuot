"""
Constants used throughout the bot.
"""

# Bot Configuration
BOT_PREFIX = '+'
BOT_DESCRIPTION = 'A multipurpose Discord bot'
BOT_VERSION = '1.0.0'

# URLs
KEEPALIVE_URL = 'https://bot-chuot-uw6x.onrender.com'

# File Paths
RULES_FILE_PATH = 'src/txt_files/100_rules_of_internet.txt'

# Command Categories
CATEGORY_FUN = 'fun'
CATEGORY_GENERAL = 'general'
CATEGORY_SLASH = 'slash'
CATEGORY_NONSLASH = 'non-slash'

# Command Directories
COMMAND_DIRECTORIES = [
    './src/commands/non-slash',
    './src/commands/fun',
    './src/commands/slash',
    './src/commands/general',
]



# Other Extension Directories
OTHER_EXTENSION_DIRECTORIES = [
    './src/status',
    './src/message'
]

# Required Extensions (only these will be loaded)
REQUIRED_EXTENSIONS = {
    'status': ['activity'],
    'message': ['response']
}

# Embed Colors
DEFAULT_EMBED_COLOR = 0x3498db  # Blue
SUCCESS_EMBED_COLOR = 0x2ecc71  # Green
ERROR_EMBED_COLOR = 0xe74c3c    # Red
WARNING_EMBED_COLOR = 0xf1c40f  # Yellow
INFO_EMBED_COLOR = 0x9b59b6     # Purple 

CATEGORY_NAMES = {
    'fun': 'Fun',
    'general': 'General',
    'slash': 'Slash',
    'non-slash': 'Non-Slash'
} 