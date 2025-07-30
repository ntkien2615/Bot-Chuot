"""
UI View và logic game cho Russian Roulette
"""
import discord
import random
import asyncio
from typing import List

from .gun_types import GunType
from .utils import create_result_embed, create_winner_embed


class GunGameView(discord.ui.View):
    """View cho trò chơi súng với buttons"""
    
    def __init__(self, players: List[discord.Member], gun_type: GunType, host: discord.Member):
        super().__init__(timeout=300)  # 5 phút timeout
        self.players = players
        self.gun_type = gun_type
        self.host = host
        self.current_player_index = 0
        self.game_over = False
        self.chambers = []
        self.round_number = 1
        self.survivors = players.copy()
        self.used_chambers = []
        
        # Tạo các chamber (viên đạn)
        self.setup_chambers()
        
        # Tạo buttons cho chambers
        self.create_chamber_buttons()
    
    def setup_chambers(self):
        """Thiết lập các viên đạn trong chambers"""
        self.chambers = ['💥'] * self.gun_type.bullets + ['🔫'] * (self.gun_type.chambers - self.gun_type.bullets)
        random.shuffle(self.chambers)
        print(f"Chambers setup: {self.chambers}")  # Debug
    
    def create_chamber_buttons(self):
        """Tạo buttons cho các chamber"""
        # Chia chambers thành rows để không vượt quá 5 buttons/row
        chambers_per_row = 5
        total_chambers = min(self.gun_type.chambers, 20)  # Discord giới hạn 25 components
        
        for i in range(total_chambers):
            button = discord.ui.Button(
                label=f"🎯 {i+1}",
                style=discord.ButtonStyle.secondary,
                custom_id=f"chamber_{i}",
                row=i // chambers_per_row  # Phân bố vào các hàng
            )
            button.callback = self.create_chamber_callback(i)
            self.add_item(button)
        
        # Thêm button Exit Game
        exit_button = discord.ui.Button(
            label="🚪 Thoát Game",
            style=discord.ButtonStyle.danger,
            custom_id="exit_game",
            row=4  # Đặt ở hàng cuối
        )
        exit_button.callback = self.exit_game_callback
        self.add_item(exit_button)
    
    def create_chamber_callback(self, chamber_index: int):
        """Tạo callback function cho từng chamber button"""
        async def chamber_callback(interaction: discord.Interaction):
            await self.handle_chamber_click(interaction, chamber_index)
        return chamber_callback
    
    async def handle_chamber_click(self, interaction: discord.Interaction, chamber_id: int):
        """Xử lý khi người chơi bấm vào chamber"""
        # Kiểm tra quyền
        if interaction.user != self.survivors[self.current_player_index]:
            await interaction.response.send_message(
                f"❌ Không phải lượt của bạn! Lượt hiện tại: {self.survivors[self.current_player_index].mention}",
                ephemeral=True
            )
            return
        
        if self.game_over:
            await interaction.response.send_message("🎮 Trò chơi đã kết thúc!", ephemeral=True)
            return
        
        if chamber_id in self.used_chambers:
            await interaction.response.send_message("❌ Chamber này đã được sử dụng!", ephemeral=True)
            return
        
        if chamber_id >= len(self.chambers):
            await interaction.response.send_message("❌ Chamber không hợp lệ!", ephemeral=True)
            return
        
        # Lấy kết quả
        current_player = self.survivors[self.current_player_index]
        chamber_result = self.chambers[chamber_id]
        self.used_chambers.append(chamber_id)
        
        # Cập nhật button
        for item in self.children:
            if hasattr(item, 'custom_id') and item.custom_id == f"chamber_{chamber_id}":
                item.disabled = True
                if chamber_result == '💥':
                    item.label = f"💥 {chamber_id+1}"
                    item.style = discord.ButtonStyle.danger
                else:
                    item.label = f"✅ {chamber_id+1}"
                    item.style = discord.ButtonStyle.success
                break
        
        # Tạo embed kết quả
        is_death = chamber_result == '💥'
        embed = create_result_embed(current_player, chamber_id, chamber_result, self.gun_type, is_death)
        
        if is_death:
            # Người chơi bị loại
            self.survivors.remove(current_player)
            
            # Kiểm tra điều kiện thắng
            if len(self.survivors) <= 1:
                self.game_over = True
                
                # Merge embed với kết quả cuối game
                winner_embed = create_winner_embed(self.survivors[0] if self.survivors else None)
                
                # Combine thông tin
                embed.add_field(
                    name=winner_embed.title,
                    value=winner_embed.description,
                    inline=False
                )
                
                if self.survivors:
                    embed.color = discord.Color.gold()
                
                # Disable tất cả buttons
                for item in self.children:
                    if hasattr(item, 'disabled'):
                        item.disabled = True
                        
            else:
                # Reset current_player_index nếu cần
                if self.current_player_index >= len(self.survivors):
                    self.current_player_index = 0
        else:
            # Người chơi an toàn, chuyển lượt
            self.current_player_index = (self.current_player_index + 1) % len(self.survivors)
        
        # Cập nhật thông tin lượt tiếp theo
        if not self.game_over and self.survivors:
            next_player = self.survivors[self.current_player_index]
            embed.add_field(
                name="🎯 Lượt tiếp theo", 
                value=f"{next_player.mention}",
                inline=True
            )
            embed.add_field(
                name="🔢 Chambers còn lại", 
                value=f"{len(self.chambers) - len(self.used_chambers)}",
                inline=True
            )
            embed.add_field(
                name="👥 Người sống", 
                value=f"{len(self.survivors)}",
                inline=True
            )
        
        await interaction.response.edit_message(embed=embed, view=self)
    
    async def exit_game_callback(self, interaction: discord.Interaction):
        """Xử lý thoát game"""
        if interaction.user != self.host:
            await interaction.response.send_message(
                "❌ Chỉ host mới có thể thoát game!",
                ephemeral=True
            )
            return
        
        # Tạo embed thông báo thoát
        embed = discord.Embed(
            title="🚪 Game đã kết thúc",
            description=f"Host {self.host.mention} đã thoát game.",
            color=discord.Color.orange()
        )
        
        embed.add_field(
            name="📊 Thống kê cuối game",
            value=f"**Người sống sót:** {len(self.survivors)}\n"
                  f"**Chambers đã dùng:** {len(self.used_chambers)}/{self.gun_type.chambers}",
            inline=False
        )
        
        # Disable tất cả buttons
        for item in self.children:
            if hasattr(item, 'disabled'):
                item.disabled = True
        
        self.game_over = True
        await interaction.response.edit_message(embed=embed, view=self)
    
    async def on_timeout(self):
        """Xử lý khi view timeout"""
        # Disable tất cả buttons
        for item in self.children:
            if hasattr(item, 'disabled'):
                item.disabled = True
        
        # Note: Không thể edit message ở đây vì không có interaction
