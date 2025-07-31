"""
Kiss command - Send a kiss to another user
"""
import discord
from discord.ext import commands
from discord import app_commands
import random
from typing import Optional

from src.commands.base_command import FunCommand


class KissSlash(FunCommand):
    """Command để hôn người khác với ảnh cute"""

    def __init__(self, discord_bot):
        super().__init__(discord_bot)
    
    def get_kiss_url_from_file(self, file_path: str = "src/txt_files/kiss.txt") -> Optional[str]:
        """Đọc URL ảnh kiss từ file txt"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f.readlines() if line.strip()]
            
            if lines:
                return random.choice(lines)
            return None
            
        except (FileNotFoundError, IOError) as e:
            print(f"Error reading kiss file {file_path}: {e}")
            return None

    @app_commands.command(name='kiss', description='💋 Hôn một người nào đó với ảnh dễ thương')
    @app_commands.describe(user='👤 Người bạn muốn hôn')
    async def kiss_command(self, interaction: discord.Interaction, user: Optional[discord.Member] = None):
        """Command chính để hôn người khác"""
        
        # Kiểm tra user hợp lệ
        if user is None:
            embed = discord.Embed(
                title="❌ Thiếu thông tin",
                description="Bạn cần chọn một người để hôn!",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        if user == interaction.user:
            embed = discord.Embed(
                title="🤔 Tự hôn mình?",
                description="Bạn không thể tự hôn chính mình được đâu!",
                color=discord.Color.orange()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        if user.bot:
            embed = discord.Embed(
                title="🤖 Bot không cần hôn",
                description="Bot không cần được hôn đâu!",
                color=discord.Color.blue()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        try:
            # Lấy ảnh kiss
            kiss_url = await self.get_kiss_image()
            
            if kiss_url:
                embed = discord.Embed(
                    title="💋 Kiss!",
                    description=f"**{interaction.user.mention}** đã hôn **{user.mention}** 😘💕",
                    color=discord.Color.pink()
                )
                embed.set_image(url=kiss_url)
                embed.set_footer(
                    text=f"Được yêu cầu bởi {interaction.user.display_name}",
                    icon_url=interaction.user.display_avatar.url
                )
                
                await interaction.response.send_message(embed=embed)
            else:
                # Fallback nếu không có ảnh
                embed = discord.Embed(
                    title="💋 Kiss!",
                    description=f"**{interaction.user.mention}** đã hôn **{user.mention}** 😘💕\n"
                               f"*(Không tìm thấy ảnh, nhưng tình cảm vẫn chân thành!)*",
                    color=discord.Color.pink()
                )
                await interaction.response.send_message(embed=embed)
                
        except Exception as e:
            print(f"Error in kiss command: {e}")
            embed = discord.Embed(
                title="❌ Lỗi",
                description="Đã xảy ra lỗi khi thực hiện lệnh. Vui lòng thử lại sau!",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    async def get_kiss_image(self) -> Optional[str]:
        """Lấy URL ảnh kiss từ config hoặc file"""
        
        # Thử lấy từ config trước
        try:
            kiss_images = self.config.get_image_urls('KISS_IMAGES')
            if kiss_images and len(kiss_images) > 0:
                return random.choice(kiss_images)
        except Exception as config_error:
            print(f"Config error in kiss command: {config_error}")
        
        # Fallback: đọc từ file
        return self.get_kiss_url_from_file()