"""
Models và classes cho RPS game
"""
import discord
import asyncio
from typing import List, Dict, Optional


class RPSChoiceModal(discord.ui.Modal):
    """Modal ẩn để người chơi chọn kéo búa bao"""
    
    def __init__(self, game_view, player: discord.Member):
        super().__init__(title="Chọn kéo, búa, bao", timeout=10)
        self.game_view = game_view
        self.player = player
        
        self.choice_input = discord.ui.TextInput(
            label="Nhập lựa chọn của bạn",
            placeholder="Nhập: kéo, búa, hoặc bao",
            max_length=4,
            required=False
        )
        self.add_item(self.choice_input)
    
    async def on_submit(self, interaction: discord.Interaction):
        choice = self.choice_input.value.lower().strip()
        
        # Validate choice
        valid_choices = {
            'kéo': 'Kéo', 'keo': 'Kéo', 'k': 'Kéo',
            'búa': 'Búa', 'bua': 'Búa', 'b': 'Búa',
            'bao': 'Bao', 'giấy': 'Bao', 'g': 'Bao'
        }
        
        if choice in valid_choices:
            normalized_choice = valid_choices[choice]
            await self.game_view.submit_choice(interaction, self.player, normalized_choice)
        elif choice == "":
            await self.game_view.submit_choice(interaction, self.player, None)
        else:
            await interaction.response.send_message(
                "❌ **Lựa chọn không hợp lệ!**\n"
                "✅ Nhập: **kéo**, **búa**, hoặc **bao**\n"
                "🔥 Gợi ý: k, b, g cũng được nhé!",
                ephemeral=True
            )


class ModalSenderView(discord.ui.View):
    """View để gửi modal qua DM"""
    
    def __init__(self, modal: RPSChoiceModal):
        super().__init__(timeout=10)
        self.modal = modal
    
    @discord.ui.button(label="🎯 Chọn ngay", style=discord.ButtonStyle.primary)
    async def open_modal(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(self.modal)


def calculate_rps_results(player_choices: Dict[discord.Member, Optional[str]]) -> Dict:
    """Tính toán kết quả game RPS"""
    # Thống kê lựa chọn
    stats = {"Kéo": 0, "Búa": 0, "Bao": 0, "None": 0}
    active_players = {}  # Chỉ tính những người chọn
    
    for player, choice in player_choices.items():
        if choice:
            stats[choice] += 1
            active_players[player] = choice
        else:
            stats["None"] += 1
    
    # Nếu không có ai chọn hoặc chỉ có 1 người chọn
    if len(active_players) <= 1:
        return {"winners": [], "stats": stats}
    
    # Kiểm tra các lựa chọn duy nhất
    unique_choices = set(active_players.values())
    
    # Nếu tất cả chọn giống nhau -> hòa
    if len(unique_choices) == 1:
        return {"winners": [], "stats": stats}
    
    # Nếu có cả 3 lựa chọn -> hòa
    if len(unique_choices) == 3:
        return {"winners": [], "stats": stats}
    
    # Nếu có 2 lựa chọn -> xác định người thắng
    choices = list(unique_choices)
    if set(choices) == {"Kéo", "Búa"}:
        winners = [p for p, c in active_players.items() if c == "Búa"]
    elif set(choices) == {"Búa", "Bao"}:
        winners = [p for p, c in active_players.items() if c == "Bao"]
    elif set(choices) == {"Bao", "Kéo"}:
        winners = [p for p, c in active_players.items() if c == "Kéo"]
    else:
        winners = []
    
    return {"winners": winners, "stats": stats}
