"""
Views cho RPS multiplayer game
"""
import discord
import random
import asyncio
from typing import List, Dict, Optional

from .rps_models import RPSButtonView, calculate_rps_results


class MultiplayerRPSView(discord.ui.View):
    """View cho game RPS nhiều người chơi"""
    
    def __init__(self, players: List[discord.Member], host: discord.Member):
        super().__init__(timeout=15)
        self.players = players
        self.host = host
        self.player_choices: Dict[discord.Member, Optional[str]] = {}
        self.results_shown = False
    
    async def start_choice_phase(self, interaction: discord.Interaction):
        """Bắt đầu giai đoạn chọn"""
        embed = self.create_choice_embed()
        await interaction.response.edit_message(embed=embed, view=self)
        
        # Gửi button interface cho từng người chơi
        for player in self.players:
            try:
                # Chỉ gửi buttons, không có modal text nữa
                button_view = RPSButtonView(self, player)
                
                embed = discord.Embed(
                    title="🎮 ROCK PAPER SCISSORS",
                    description=f"⏰ **{player.display_name}**, hãy chọn kéo, búa hoặc bao!\n"
                               f"🕐 Bạn có **30 giây** để suy nghĩ và chọn.",
                    color=discord.Color.blue()
                )
                
                embed.add_field(
                    name="🎯 Cách chơi",
                    value="✂️ **Kéo** → thắng Bao\n"
                          "🪨 **Búa** → thắng Kéo\n"
                          "📄 **Bao** → thắng Búa",
                    inline=True
                )
                
                embed.add_field(
                    name="⚡ Lưu ý",
                    value="• Nhấn nút để chọn nhanh\n"
                          "• Chỉ được chọn 1 lần!\n"
                          "• Nút sẽ tắt sau khi chọn",
                    inline=True
                )
                
                # Chỉ gửi buttons interface
                await player.send(embed=embed, view=button_view)
                
            except discord.Forbidden:
                self.player_choices[player] = None
        
        # Bắt đầu countdown và cập nhật realtime
        await self.countdown_and_update(interaction)
    
    def create_choice_embed(self) -> discord.Embed:
        """Tạo embed cho giai đoạn chọn"""
        embed = discord.Embed(
            title="✂️ 🪨 📄 ROCK PAPER SCISSORS",
            description="🎯 **Người chơi đang chọn lựa trong tin nhắn riêng!**\n"
                       "⚡ Hãy suy nghĩ kỹ trước khi quyết định...",
            color=discord.Color.orange()
        )
        
        # Danh sách người chơi với trạng thái
        player_list = []
        for i, player in enumerate(self.players, 1):
            status = "✅" if player in self.player_choices else "⏳"
            player_list.append(f"{status} {i}. {player.display_name}")
        
        embed.add_field(
            name="👥 Danh sách người chơi",
            value="\n".join(player_list),
            inline=False
        )
        
        chosen_count = len(self.player_choices)
        progress_bar = "🟩" * chosen_count + "⬜" * (len(self.players) - chosen_count)
        
        embed.add_field(
            name="📊 Tiến độ",
            value=f"{progress_bar}\n**Đã chọn: {chosen_count}/{len(self.players)}**",
            inline=False
        )
        
        embed.set_footer(
            text="💡 Kiểm tra tin nhắn riêng để chọn kéo, búa, hoặc bao!"
        )
        
        return embed
    
    async def countdown_and_update(self, interaction: discord.Interaction):
        """Countdown 30 giây và cập nhật realtime"""
        for remaining in range(30, 0, -1):
            if len(self.player_choices) >= len(self.players):
                break
                
            embed = self.create_choice_embed()
            embed.description = f"Các người chơi đang chọn kéo, búa, bao trong tin nhắn riêng!\n⏰ Còn lại: {remaining} giây"
            
            try:
                await interaction.edit_original_response(embed=embed, view=self)
            except:
                pass
                
            await asyncio.sleep(1)
        
        await self.end_choice_phase(interaction)
    
    async def submit_choice(self, interaction: discord.Interaction, player: discord.Member, choice: Optional[str]):
        """Xử lý khi người chơi submit choice"""
        if player not in self.players:
            await interaction.response.send_message("❌ Bạn không trong game này!", ephemeral=True)
            return
        
        if player in self.player_choices:
            await interaction.response.send_message("❌ Bạn đã chọn rồi!", ephemeral=True)
            return
        
        self.player_choices[player] = choice
        
        if choice:
            await interaction.response.send_message(f"✅ Đã chọn: {choice}", ephemeral=True)
        else:
            await interaction.response.send_message("✅ Đã bỏ qua lượt chọn", ephemeral=True)
    
    async def end_choice_phase(self, interaction: discord.Interaction):
        """Kết thúc giai đoạn chọn và hiển thị kết quả"""
        if self.results_shown:
            return
        
        self.results_shown = True
        
        # Đảm bảo tất cả người chơi có choice
        for player in self.players:
            if player not in self.player_choices:
                self.player_choices[player] = None
        
        results = calculate_rps_results(self.player_choices)
        embed = self.create_results_embed(results)
        
        # Disable tất cả buttons
        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True
        
        try:
            await interaction.edit_original_response(embed=embed, view=self)
        except:
            pass
    
    def create_results_embed(self, results: Dict) -> discord.Embed:
        """Tạo embed kết quả"""
        embed = discord.Embed(
            title="🏆 ROCK PAPER SCISSORS - KẾT QUẢ!",
            color=discord.Color.green()
        )
        
        # Hiển thị lựa chọn với emoji đẹp
        choices_text = ""
        choice_emojis = {"Kéo": "✂️", "Búa": "🪨", "Bao": "📄"}
        
        for i, player in enumerate(self.players, 1):
            choice = self.player_choices[player]
            if choice:
                emoji = choice_emojis[choice]
                choices_text += f"{emoji} **{i}.** {player.display_name} → **{choice}**\n"
            else:
                choices_text += f"❌ **{i}.** {player.display_name} → *(không chọn)*\n"
        
        embed.add_field(
            name="🎯 Lựa chọn của mọi người",
            value=choices_text,
            inline=False
        )
        
        # Hiển thị kết quả với style đẹp
        if results["winners"]:
            winner_names = [f"🎉 **{w.display_name}**" for w in results["winners"]]
            winners_text = "\n".join(winner_names)
            
            embed.add_field(
                name="🏆 NGƯỜI THẮNG CUỘC!",
                value=winners_text,
                inline=True
            )
            
            embed.add_field(
                name="🎊 Chúc mừng!",
                value="Bạn đã chơi rất xuất sắc!",
                inline=True
            )
        else:
            embed.add_field(
                name="🤝 KẾT QUẢ HÒA!",
                value="🎭 Tất cả mọi người đều chọn giống nhau\n"
                      "hoặc không có ai thắng được ai!",
                inline=False
            )
            
        # Thêm thông tin thống kê
        total_players = len(self.players)
        active_players = len([p for p in self.player_choices.values() if p])
        
        embed.add_field(
            name="📊 Thống kê game",
            value=f"👥 Tổng người chơi: **{total_players}**\n"
                  f"🎯 Đã tham gia: **{active_players}**\n"
                  f"⏱️ Thời gian: **30 giây**",
            inline=False
        )
        
        embed.set_footer(
            text="🎮 Cảm ơn bạn đã chơi Rock Paper Scissors!"
        )
        
        # Thống kê
        stats = results['stats']
        stats_text = f"✂️ Kéo: {stats['Kéo']} • 🔨 Búa: {stats['Búa']} • 📄 Bao: {stats['Bao']} • ❌ Bỏ qua: {stats['None']}"
        embed.add_field(name="📊 Thống kê", value=stats_text, inline=False)
        
        embed.set_footer(text=f"Host: {self.host.display_name}")
        return embed


class InviteRPSView(discord.ui.View):
    """View để mời người chơi tham gia RPS"""
    
    def __init__(self, host: discord.Member, max_players: int = 8):
        super().__init__(timeout=30)  # 30 giây timeout
        self.host = host
        self.max_players = max_players
        self.joined_players = [host]
        self.message: Optional[discord.Message] = None
    
    async def on_timeout(self):
        """Xử lý khi hết thời gian chờ"""
        if self.message:
            embed = discord.Embed(
                title="⏰ HẾT THỜI GIAN CHỜ",
                description=f"🎮 Game RPS đã tự động hủy sau 30 giây không có hoạt động.\n"
                           f"🎭 Host: **{self.host.display_name}**\n"
                           f"👥 Người tham gia: {len(self.joined_players)}/{self.max_players}",
                color=discord.Color.orange()
            )
            
            if len(self.joined_players) > 1:
                player_list = [f"🎮 {member.display_name}" for member in self.joined_players]
                embed.add_field(
                    name="👥 Danh sách người chơi đã tham gia",
                    value="\n".join(player_list),
                    inline=False
                )
            
            embed.add_field(
                name="💡 Cách tránh timeout",
                value="• Host có thể bắt đầu sớm với ít người\n"
                      "• Mời bạn bè nhanh hơn\n"
                      "• Hoặc thử lại lệnh /rps",
                inline=False
            )
            
            # Disable tất cả buttons
            for item in self.children:
                if isinstance(item, discord.ui.Button):
                    item.disabled = True
            
            try:
                await self.message.edit(embed=embed, view=self)
            except:
                pass
    
    def create_invite_embed(self) -> discord.Embed:
        """Tạo embed mời chơi"""
        embed = discord.Embed(
            title="🎮 ROCK PAPER SCISSORS - Mời tham gia!",
            description=f"🎭 **Host:** {self.host.display_name}\n"
                       f"🎯 **Chơi cùng nhau:** Kéo, Búa, Bao!\n"
                       f"⏰ **Thời gian chờ:** 30 giây",
            color=discord.Color.blue()
        )
        
        # Danh sách người đã tham gia
        if len(self.joined_players) > 1:
            player_list = []
            for i, player in enumerate(self.joined_players, 1):
                emoji = "👑" if player == self.host else "🎮"
                player_list.append(f"{emoji} {i}. {player.display_name}")
            
            embed.add_field(
                name=f"👥 Người tham gia ({len(self.joined_players)}/{self.max_players})",
                value="\n".join(player_list),
                inline=False
            )
        else:
            embed.add_field(
                name=f"👥 Người tham gia ({len(self.joined_players)}/{self.max_players})",
                value=f"👑 1. {self.host.display_name}\n"
                      f"⏳ Đang chờ thêm người chơi...",
                inline=False
            )
        
        embed.add_field(
            name="🎯 Cách chơi",
            value="• Nhấn **Tham gia** để vào game\n"
                  "• Host nhấn **Bắt đầu** khi đủ người\n"
                  "• Mọi người chọn kéo/búa/bao cùng lúc",
            inline=True
        )
        
        embed.add_field(
            name="🏆 Luật chơi",
            value="✂️ **Kéo** thắng **Bao**\n"
                  "🪨 **Búa** thắng **Kéo**\n"
                  "📄 **Bao** thắng **Búa**",
            inline=True
        )
        
        return embed
    
    @discord.ui.button(label="🎮 Tham gia", style=discord.ButtonStyle.primary)
    async def join_game(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Tham gia game"""
        # Kiểm tra user là Member
        if not isinstance(interaction.user, discord.Member):
            await interaction.response.send_message("❌ Lệnh này chỉ có thể sử dụng trong server!", ephemeral=True)
            return
            
        if interaction.user in self.joined_players:
            await interaction.response.send_message("🎮 Bạn đã tham gia rồi!", ephemeral=True)
            return
        
        if len(self.joined_players) >= self.max_players:
            await interaction.response.send_message("🚫 Game đã đầy người!", ephemeral=True)
            return
        
        self.joined_players.append(interaction.user)
        embed = self.create_invite_embed()
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="🚀 Bắt đầu", style=discord.ButtonStyle.success)
    async def start_game(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Bắt đầu game"""
        # Kiểm tra user là Member
        if not isinstance(interaction.user, discord.Member):
            await interaction.response.send_message("❌ Lệnh này chỉ có thể sử dụng trong server!", ephemeral=True)
            return
            
        if interaction.user != self.host:
            await interaction.response.send_message("🔒 Chỉ host mới có thể bắt đầu game!", ephemeral=True)
            return
        
        if len(self.joined_players) < 2:
            await interaction.response.send_message("👥 Cần ít nhất 2 người để chơi!", ephemeral=True)
            return
        
        # Chuyển sang MultiplayerRPSView
        game_view = MultiplayerRPSView(self.joined_players, self.host)
        await game_view.start_choice_phase(interaction)
    
    @discord.ui.button(label="❌ Rời khỏi", style=discord.ButtonStyle.secondary)
    async def leave_game(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Rời khỏi game"""
        # Kiểm tra user là Member
        if not isinstance(interaction.user, discord.Member):
            await interaction.response.send_message("❌ Lệnh này chỉ có thể sử dụng trong server!", ephemeral=True)
            return
            
        if interaction.user not in self.joined_players:
            await interaction.response.send_message("❌ Bạn chưa tham gia!", ephemeral=True)
            return
        
        if interaction.user == self.host and len(self.joined_players) > 1:
            await interaction.response.send_message("👑 Host không thể rời khi còn người chơi!", ephemeral=True)
            return
        
        self.joined_players.remove(interaction.user)
        
        if len(self.joined_players) == 0:
            # Game bị hủy
            embed = discord.Embed(
                title="🚫 GAME ĐÃ BỊ HỦY",
                description="❌ Host đã rời và không còn ai trong game.",
                color=discord.Color.red()
            )
            await interaction.response.edit_message(embed=embed, view=None)
        else:
            embed = self.create_invite_embed()
            await interaction.response.edit_message(embed=embed, view=self)
