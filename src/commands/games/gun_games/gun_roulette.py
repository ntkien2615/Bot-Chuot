"""
Command chính cho Russian Roulette Game
"""
import discord
from discord.ext import commands
from discord import app_commands
import random
from typing import List

from src.commands.base_command import GameCommand
from .gun_types import GUN_TYPES, get_gun_type, get_all_gun_choices
from .gun_game_view import GunGameView
from .utils import parse_players_from_string, validate_player_count, create_game_embed


class InviteView(discord.ui.View):
    """View để mời người chơi tham gia game"""
    
    def __init__(self, host: discord.Member, gun_type_key: str, max_players: int = 8):
        super().__init__(timeout=60)  # 1 phút để join
        self.host = host
        self.gun_type_key = gun_type_key
        self.max_players = max_players
        self.joined_players = [host]  # Host tự động join
        
    @discord.ui.button(label="🎮 Tham gia", style=discord.ButtonStyle.green, emoji="🎯")
    async def join_game(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Button để tham gia game"""
        # Kiểm tra user là Member
        if not isinstance(interaction.user, discord.Member):
            await interaction.response.send_message("❌ Chỉ có thể sử dụng trong server!", ephemeral=True)
            return
            
        if interaction.user in self.joined_players:
            await interaction.response.send_message("❌ Bạn đã tham gia rồi!", ephemeral=True)
            return
            
        if len(self.joined_players) >= self.max_players:
            await interaction.response.send_message("❌ Game đã đủ người!", ephemeral=True)
            return
            
        self.joined_players.append(interaction.user)
        
        # Cập nhật embed
        gun_type = get_gun_type(self.gun_type_key)
        if not gun_type:
            await interaction.response.send_message("❌ Lỗi loại súng!", ephemeral=True)
            return
        embed = discord.Embed(
            title=f"🎮 Russian Roulette - {gun_type.name}",
            description=f"{gun_type.description}\n\n"
                       f"**Chambers:** {gun_type.chambers}\n"
                       f"**Đạn thật:** {gun_type.bullets}\n"
                       f"**Tỷ lệ sống:** {gun_type.survival_rate:.1f}%",
            color=discord.Color.blue()
        )
        
        player_list = "\n".join([f"{i+1}. {member.mention}" for i, member in enumerate(self.joined_players)])
        embed.add_field(
            name=f"👥 Người chơi ({len(self.joined_players)}/{self.max_players})",
            value=player_list,
            inline=False
        )
        
        embed.add_field(
            name="📝 Hướng dẫn",
            value="• Bấm 🎮 để tham gia\n• Host bấm 🚀 để bắt đầu\n• Cần ít nhất 2 người",
            inline=False
        )
        
        embed.set_footer(text=f"Host: {self.host.display_name}")
        
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="🚀 Bắt đầu", style=discord.ButtonStyle.primary, emoji="🎯")
    async def start_game(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Button để bắt đầu game"""
        if interaction.user != self.host:
            await interaction.response.send_message("❌ Chỉ host mới có thể bắt đầu!", ephemeral=True)
            return
            
        is_valid, error_msg = validate_player_count(self.joined_players)
        if not is_valid:
            await interaction.response.send_message(error_msg, ephemeral=True)
            return
        
        # Xáo trộn thứ tự người chơi
        random.shuffle(self.joined_players)
        
        gun_type = get_gun_type(self.gun_type_key)
        if not gun_type:
            await interaction.response.send_message("❌ Lỗi loại súng!", ephemeral=True)
            return
            
        embed = create_game_embed(gun_type, self.joined_players, self.joined_players[0])
        
        # Tạo game view
        game_view = GunGameView(self.joined_players, gun_type, self.host)
        
        await interaction.response.edit_message(embed=embed, view=game_view)
    
    @discord.ui.button(label="❌ Hủy", style=discord.ButtonStyle.danger, emoji="🚫")
    async def cancel_game(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Button để hủy game"""
        if interaction.user != self.host:
            await interaction.response.send_message("❌ Chỉ host mới có thể hủy!", ephemeral=True)
            return
        
        embed = discord.Embed(
            title="❌ Game đã bị hủy",
            description=f"Host {self.host.mention} đã hủy game.",
            color=discord.Color.red()
        )
        
        # Disable tất cả buttons
        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True
        
        await interaction.response.edit_message(embed=embed, view=self)


class GunRoulette(GameCommand):
    """Russian Roulette game với nhiều loại súng khác nhau"""
    
    def __init__(self, discord_bot):
        super().__init__(discord_bot)
    
    @app_commands.command(
        name='gun_roulette',
        description='Chơi Russian Roulette với bạn bè - nhiều loại súng khác nhau!'
    )
    @app_commands.describe(
        gun_type='Chọn loại súng để chơi',
        max_players='Số người chơi tối đa (2-8)'
    )
    @app_commands.choices(gun_type=get_all_gun_choices())
    async def gun_roulette(
        self,
        interaction: discord.Interaction,
        gun_type: str = "revolver",
        max_players: int = 8
    ):
        """Command chính để tạo game Russian Roulette"""
        
        # Kiểm tra guild
        if not interaction.guild:
            await interaction.response.send_message(
                "❌ Lệnh này chỉ có thể sử dụng trong server!",
                ephemeral=True
            )
            return
        
        # Kiểm tra user là Member
        if not isinstance(interaction.user, discord.Member):
            await interaction.response.send_message(
                "❌ Lỗi: Không thể xác định thông tin người dùng!",
                ephemeral=True
            )
            return
        
        # Kiểm tra max_players
        if max_players < 2 or max_players > 8:
            await interaction.response.send_message(
                "❌ Số người chơi tối đa phải từ 2 đến 8!",
                ephemeral=True
            )
            return
        
        # Kiểm tra gun type
        selected_gun = get_gun_type(gun_type)
        if not selected_gun:
            await interaction.response.send_message(
                "❌ Loại súng không hợp lệ!",
                ephemeral=True
            )
            return
        
        # Tạo embed mời chơi
        embed = discord.Embed(
            title=f"🎮 Russian Roulette - {selected_gun.name}",
            description=f"{selected_gun.description}\n\n"
                       f"**Chambers:** {selected_gun.chambers}\n"
                       f"**Đạn thật:** {selected_gun.bullets}\n"
                       f"**Tỷ lệ sống:** {selected_gun.survival_rate:.1f}%",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name=f"👥 Người chơi (1/{max_players})",
            value=f"1. {interaction.user.mention}",
            inline=False
        )
        
        embed.add_field(
            name="📝 Hướng dẫn",
            value="• Bấm 🎮 để tham gia\n• Host bấm 🚀 để bắt đầu\n• Cần ít nhất 2 người",
            inline=False
        )
        
        embed.set_footer(text=f"Host: {interaction.user.display_name}")
        
        # Tạo invite view
        invite_view = InviteView(interaction.user, gun_type, max_players)
        
        await interaction.response.send_message(embed=embed, view=invite_view)
    
    @app_commands.command(
        name='gun_quick',
        description='Chơi Russian Roulette nhanh với những người được mention'
    )
    @app_commands.describe(
        players='Mention những người muốn chơi (ví dụ: @user1 @user2)',
        gun_type='Chọn loại súng để chơi'
    )
    @app_commands.choices(gun_type=get_all_gun_choices())
    async def gun_quick(
        self,
        interaction: discord.Interaction,
        players: str,
        gun_type: str = "revolver"
    ):
        """Command để tạo game nhanh với người được mention"""
        
        # Kiểm tra guild
        if not interaction.guild:
            await interaction.response.send_message(
                "❌ Lệnh này chỉ có thể sử dụng trong server!",
                ephemeral=True
            )
            return
        
        # Kiểm tra user là Member
        if not isinstance(interaction.user, discord.Member):
            await interaction.response.send_message(
                "❌ Lỗi: Không thể xác định thông tin người dùng!",
                ephemeral=True
            )
            return
        
        # Parse người chơi
        members = parse_players_from_string(players, interaction.guild, interaction.user)
        
        # Validate
        is_valid, error_msg = validate_player_count(members)
        if not is_valid:
            await interaction.response.send_message(error_msg, ephemeral=True)
            return
        
        # Kiểm tra gun type
        selected_gun = get_gun_type(gun_type)
        if not selected_gun:
            await interaction.response.send_message(
                "❌ Loại súng không hợp lệ!",
                ephemeral=True
            )
            return
        
        # Xáo trộn thứ tự người chơi
        random.shuffle(members)
        
        # Tạo game ngay lập tức
        embed = create_game_embed(selected_gun, members, members[0])
        game_view = GunGameView(members, selected_gun, interaction.user)  # interaction.user đã được validate là Member ở trên
        
        await interaction.response.send_message(embed=embed, view=game_view)


async def setup(bot):
    """Setup function để load cog"""
    await bot.add_cog(GunRoulette(bot))
