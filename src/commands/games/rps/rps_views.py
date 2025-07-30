"""
Views cho RPS multiplayer game
"""
import discord
import random
import asyncio
from typing import List, Dict, Optional

from .rps_models import RPSChoiceModal, ModalSenderView, calculate_rps_results


class MultiplayerRPSView(discord.ui.View):
    """View cho game RPS nhiều người chơi"""
    
    def __init__(self, players: List[discord.Member], host: discord.Member):
        super().__init__(timeout=15)
        self.players = players
        self.host = host
        self.player_choices: Dict[discord.Member, Optional[str]] = {}
        self.game_started = False
        self.choice_phase = False
        self.results_shown = False
        self.choice_start_time = None
        
    async def start_choice_phase(self, interaction: discord.Interaction):
        """Bắt đầu giai đoạn chọn"""
        self.choice_phase = True
        self.game_started = True
        self.choice_start_time = asyncio.get_event_loop().time()
        
        # Disable start button
        for item in self.children:
            if isinstance(item, discord.ui.Button) and item.label == "🚀 Bắt đầu":
                item.disabled = True
        
        embed = self.create_choice_embed()
        await interaction.response.edit_message(embed=embed, view=self)
        
        # Gửi modal cho từng người chơi
        for player in self.players:
            try:
                modal = RPSChoiceModal(self, player)
                await player.send("🎮 Thời gian chọn cho game Rock Paper Scissors!", 
                                view=ModalSenderView(modal))
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
        """Countdown 10 giây và cập nhật realtime"""
        for remaining in range(10, 0, -1):
            if len(self.player_choices) >= len(self.players):
                break
                
            embed = self.create_choice_embed()
            embed.description = f"Các người chọi đang chọn kéo, búa, bao trong tin nhắn riêng!\n⏰ Còn lại: {remaining} giây"
            
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
            title="� ROCK PAPER SCISSORS - KẾT QUẢ!",
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
                  f"⏱️ Thời gian: **10 giây**",
            inline=False
        )
        
        embed.set_footer(
            text="🎮 Cảm ơn bạn đã chơi Rock Paper Scissors!",
            icon_url="https://cdn.discordapp.com/emojis/🎮.png"
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
            
            embed.set_footer(text="💡 Hãy tạo game mới để chơi tiếp!")
            
            # Disable tất cả buttons
            for item in self.children:
                if isinstance(item, discord.ui.Button):
                    item.disabled = True
            
            try:
                await self.message.edit(embed=embed, view=self)
            except discord.NotFound:
                pass  # Message đã bị xóa
        
    @discord.ui.button(label="� Tham gia", style=discord.ButtonStyle.green, emoji="🎮")
    async def join_game(self, interaction: discord.Interaction, button: discord.ui.Button):
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
        embed = self.create_invite_embed()
        await interaction.response.edit_message(embed=embed, view=self)
    
    def create_invite_embed(self) -> discord.Embed:
        """Tạo embed mời chơi"""
        embed = discord.Embed(
            title="✂️ 🪨 📄 ROCK PAPER SCISSORS",
            description="🎯 **Game đối kháng nhiều người chơi!**\n"
                       "🔥 Mọi người sẽ chọn bí mật trong tin nhắn riêng\n"
                       "⚡ Ai có lựa chọn thông minh nhất sẽ thắng!",
            color=discord.Color.gold()
        )
        
        player_list = [f"🎮 {i+1}. {member.display_name}" for i, member in enumerate(self.joined_players)]
        
        embed.add_field(
            name=f"👥 Người chơi ({len(self.joined_players)}/{self.max_players})",
            value="\n".join(player_list),
            inline=False
        )
        
        embed.add_field(
            name="📋 Luật chơi",
            value="🪨 **Búa** thắng **Kéo** ✂️\n"
                  "✂️ **Kéo** thắng **Bao** 📄\n" 
                  "📄 **Bao** thắng **Búa** 🪨",
            inline=True
        )
        
        embed.add_field(
            name="🎮 Hướng dẫn",
            value="• 🎯 Bấm **Tham gia** để vào game\n"
                  "• 🚀 Host bấm **Bắt đầu** khi đủ người\n"
                  "• ⏰ Có 10 giây để chọn\n"
                  "• 🏆 Kết quả sẽ được công bố\n"
                  "• ⚠️ Game tự hủy sau 30s nếu không hoạt động",
            inline=True
        )
        
        embed.set_footer(
            text=f"🎭 Host: {self.host.display_name} | Cần ít nhất 2 người chơi",
            icon_url=self.host.display_avatar.url
        )
        
        return embed
    
    @discord.ui.button(label="🚀 Bắt đầu", style=discord.ButtonStyle.primary, emoji="⚡")
    async def start_game(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.host:
            await interaction.response.send_message("❌ Chỉ host mới có thể bắt đầu!", ephemeral=True)
            return
            
        if len(self.joined_players) < 2:
            await interaction.response.send_message("❌ Cần ít nhất 2 người chơi!", ephemeral=True)
            return
        
        # Stop timeout vì game đã bắt đầu
        self.stop()
        
        # Tạo MultiplayerRPSView mới để bắt đầu game
        game_view = MultiplayerRPSView(self.joined_players, self.host)
        await game_view.start_choice_phase(interaction)
    
    @discord.ui.button(label="❌ Hủy game", style=discord.ButtonStyle.danger, emoji="🛑")
    async def cancel_game(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.host:
            await interaction.response.send_message("❌ Chỉ host mới có thể hủy!", ephemeral=True)
            return
        
        # Stop timeout vì game đã bị hủy
        self.stop()
        
        embed = discord.Embed(
            title="🛑 GAME ĐÃ BỊ HỦY",
            description=f"🎭 Host **{self.host.display_name}** đã hủy game.\n"
                       "🎮 Hãy tạo game mới để chơi tiếp!",
            color=discord.Color.red()
        )
        
        embed.set_footer(text="Cảm ơn mọi người đã quan tâm!")
        
        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True
        
        await interaction.response.edit_message(embed=embed, view=self)
