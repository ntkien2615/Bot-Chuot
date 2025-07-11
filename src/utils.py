import discord
import random
import os
import re
import json
from datetime import datetime
import traceback


class EmbedBuilder:
    """Utility class for building Discord embeds."""
    
    @staticmethod
    def build_basic_embed(title, description, color=None):
        """Build a basic embed with title and description."""
        if color is None:
            color = discord.Color.random()
            
        return discord.Embed(
            title=title,
            description=description,
            color=color,
            timestamp=datetime.now()
        )
    
    @staticmethod
    def build_error_embed(error_message, error_details=None):
        """Build an error embed."""
        embed = discord.Embed(
            title="Đã xảy ra lỗi",
            description=str(error_message),
            color=discord.Color.red(),
            timestamp=datetime.now()
        )
        
        if error_details:
            embed.add_field(name="Chi tiết", value=str(error_details), inline=False)
            
        return embed
    
    @staticmethod
    def build_success_embed(message):
        """Build a success embed."""
        return discord.Embed(
            title="Thành công",
            description=str(message),
            color=discord.Color.green(),
            timestamp=datetime.now()
        )


class MessageUtils:
    """Utility class for handling messages."""
    
    @staticmethod
    async def send_paginated_message(ctx, content, max_chars=2000):
        """Send a message that exceeds the character limit in multiple parts."""
        if len(content) <= max_chars:
            return await ctx.send(content)
            
        parts = []
        current_part = ""
        
        for line in content.split('\n'):
            if len(current_part) + len(line) + 1 > max_chars:
                parts.append(current_part)
                current_part = line
            else:
                if current_part:
                    current_part += '\n'
                current_part += line
                
        if current_part:
            parts.append(current_part)
            
        messages = []
        for i, part in enumerate(parts):
            message = await ctx.send(f"[{i+1}/{len(parts)}]\n{part}")
            messages.append(message)
            
        return messages


class FileUtils:
    """Utility class for file operations."""
    
    @staticmethod
    def ensure_directory_exists(directory):
        """Ensure a directory exists, create it if it doesn't."""
        if not os.path.exists(directory):
            os.makedirs(directory)
            return True
        return False
    
    @staticmethod
    def read_json_file(file_path, default=None):
        """Read a JSON file safely."""
        if default is None:
            default = {}
            
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return default
        except Exception as e:
            print(f"Error reading JSON file {file_path}: {e}")
            return default
    
    @staticmethod
    def write_json_file(file_path, data):
        """Write data to a JSON file safely."""
        try:
            directory = os.path.dirname(file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
                
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            return True
        except Exception as e:
            print(f"Error writing JSON file {file_path}: {e}")
            traceback.print_exc()
            return False


class TimeUtils:
    """Utility class for time operations."""
    
    @staticmethod
    def format_duration(seconds):
        """Format a duration in seconds to a human-readable string."""
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        
        parts = []
        if days > 0:
            parts.append(f"{int(days)} ngày")
        if hours > 0:
            parts.append(f"{int(hours)} giờ")
        if minutes > 0:
            parts.append(f"{int(minutes)} phút")
        if seconds > 0 or not parts:
            parts.append(f"{int(seconds)} giây")
            
        return " ".join(parts)
    
    @staticmethod
    def get_timestamp():
        """Get current timestamp."""
        return datetime.now().timestamp()
    
    @staticmethod
    def get_formatted_time():
        """Get current time formatted."""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S") 