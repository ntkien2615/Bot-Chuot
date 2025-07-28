"""
Discord UI views for PvP game
Handles buttons, interactions, and user interface
"""

import discord
from typing import Optional
import asyncio
import time
from .player import Player
from .game_logic import GameLogic
from .constants import GameConstants, EmbedColors, Emojis, DamageType


class GameView(discord.ui.View):
    """Main game view with combat buttons"""
    
    def __init__(self, player1, player2):
        super().__init__(timeout=GameConstants.GAME_TIMEOUT)
        self.player1 = Player(player1)
        self.player2 = Player(player2)
        
        # Random người chơi đầu tiên để công bằng
        import random
        self.current_turn = random.choice([self.player1, self.player2])
        self.last_action = f"🎲 {self.current_turn.user.display_name} được quyền đánh trước!"
        self.game_over = False
        self.turn_count = 0  # Đếm số turn để cân bằng energy
        
        # AFK tracking
        self.last_action_time = time.time()
        self.afk_task = None
        self.current_message = None  # Store current message for AFK updates
        self.start_afk_timer()
    
    def switch_turn(self):
        """Switch to next player and handle energy regeneration"""
        self.turn_count += 1
        
        # Cân bằng energy regeneration
        if self.turn_count == 1:
            # Turn đầu tiên: chỉ người không đánh trước mới hồi energy
            if self.current_turn == self.player1:
                self.player2.regenerate_energy()  # Player 2 hồi energy vì bị đánh trước
            else:
                self.player1.regenerate_energy()  # Player 1 hồi energy vì bị đánh trước
        else:
            # Các turn sau: người vừa kết thúc lượt hồi energy như bình thường
            self.current_turn.regenerate_energy()
        
        # Switch to next player
        self.current_turn = self.player2 if self.current_turn == self.player1 else self.player1
        
        # Reset AFK timer for new turn
        self.reset_afk_timer()
    
    def start_afk_timer(self):
        """Start AFK timer for current player"""
        if self.afk_task:
            self.afk_task.cancel()
        self.afk_task = asyncio.create_task(self.check_afk())
    
    def reset_afk_timer(self):
        """Reset AFK timer"""
        self.last_action_time = time.time()
        self.start_afk_timer()
    
    async def check_afk(self):
        """Check if current player is AFK"""
        try:
            start_time = self.last_action_time
            await asyncio.sleep(GameConstants.AFK_TIMEOUT)
            
            # Check if game is still active and timer hasn't been reset
            if not self.game_over and self.last_action_time == start_time:
                await self.handle_afk_timeout()
        except asyncio.CancelledError:
            # Timer was cancelled (player made an action or game ended)
            pass
    
    async def handle_afk_timeout(self):
        """Handle AFK timeout - current player loses"""
        if self.game_over:
            return
            
        self.game_over = True
        afk_player = self.current_turn
        winner = self.player2 if self.current_turn == self.player1 else self.player1
        
        embed = GameLogic.create_afk_timeout_embed(afk_player, winner)
        
        # Disable all buttons
        self.clear_items()
        
        # Try to update the message if we have a reference to it
        if self.current_message:
            try:
                await self.current_message.edit(embed=embed, view=self)
            except (discord.NotFound, discord.HTTPException):
                # Message was deleted or other error, ignore
                pass
    
    async def update_game(self, interaction):
        """Update the game state and UI"""
        if self.game_over:
            return
            
        if not self.player1.is_alive() or not self.player2.is_alive():
            self.game_over = True
            winner = self.player1 if self.player1.is_alive() else self.player2
            
            # Cancel AFK timer
            if self.afk_task:
                self.afk_task.cancel()
            
            embed = GameLogic.create_victory_embed(winner, self.player1, self.player2)
            
            # Disable all buttons
            self.clear_items()
            
            try:
                await interaction.response.edit_message(embed=embed, view=self)
            except (discord.NotFound, discord.HTTPException):
                # Interaction expired or other error, ignore
                pass
            return
        
        embed = GameLogic.create_game_embed(self.player1, self.player2, self.current_turn.user, self.last_action)
        try:
            await interaction.response.edit_message(embed=embed, view=self)
            # Store message reference for AFK timeout
            if hasattr(interaction, 'message') and interaction.message:
                self.current_message = interaction.message
        except (discord.NotFound, discord.HTTPException):
            # Interaction expired or other error, ignore
            pass
    
    async def interaction_check(self, interaction):
        """Check if interaction is from current turn player"""
        if interaction.user != self.current_turn.user:
            try:
                await interaction.response.send_message("❌ Không phải lượt của bạn!", ephemeral=True)
            except (discord.NotFound, discord.HTTPException):
                # Interaction expired or other error, ignore
                pass
            return False
            
        # Reset AFK timer since player made an action
        self.reset_afk_timer()
        return True
    
    @discord.ui.button(label="👊 Đấm", style=discord.ButtonStyle.danger, emoji="👊")
    async def punch_attack(self, interaction: discord.Interaction, button: discord.ui.Button):
        player = self.current_turn
        target = self.player2 if self.current_turn == self.player1 else self.player1
        
        # Check if player has enough energy
        if not player.use_energy(GameConstants.PUNCH_ENERGY):
            try:
                await interaction.response.send_message(f"❌ Không đủ Energy! (Cần {GameConstants.PUNCH_ENERGY} Energy)", ephemeral=True)
            except (discord.NotFound, discord.HTTPException):
                # Interaction expired, ignore
                pass
            return
        
        final_damage, damage_type, action_text = GameLogic.calculate_punch_damage()
        self.last_action = f"{Emojis.PUNCH} {self.current_turn.user.display_name} {action_text}"
        
        target.take_damage(final_damage, damage_type)
        self.switch_turn()
        await self.update_game(interaction)
    
    @discord.ui.button(label="🔮 Phép", style=discord.ButtonStyle.primary, emoji="🔮")
    async def magic_attack(self, interaction: discord.Interaction, button: discord.ui.Button):
        player = self.current_turn
        target = self.player2 if self.current_turn == self.player1 else self.player1
        
        damage, energy_cost, action_text = GameLogic.calculate_magic_damage(target)
        
        # Check if player has enough energy
        if not player.use_energy(energy_cost):
            try:
                await interaction.response.send_message(f"❌ Không đủ Energy! (Cần {energy_cost} Energy)", ephemeral=True)
            except (discord.NotFound, discord.HTTPException):
                # Interaction expired, ignore
                pass
            return
        
        self.last_action = f"{Emojis.MAGIC} {self.current_turn.user.display_name} {action_text}"
        target.take_damage(damage, DamageType.MAGIC)
        
        self.switch_turn()
        await self.update_game(interaction)
    
    @discord.ui.button(label="🛡️ Giáp", style=discord.ButtonStyle.secondary, emoji="🛡️")
    async def add_armor(self, interaction: discord.Interaction, button: discord.ui.Button):
        player = self.current_turn
        
        # Check if player has enough energy
        if not player.use_energy(GameConstants.ARMOR_ENERGY):
            try:
                await interaction.response.send_message(f"❌ Không đủ Energy! (Cần {GameConstants.ARMOR_ENERGY} Energy)", ephemeral=True)
            except (discord.NotFound, discord.HTTPException):
                # Interaction expired, ignore
                pass
            return
        
        armor_amount, action_text = GameLogic.calculate_armor_gain()
        armor_gain = min(armor_amount, GameConstants.MAX_ARMOR - player.armor)
        
        if armor_amount == GameConstants.MAX_ARMOR:
            player.armor = GameConstants.MAX_ARMOR
            self.last_action = f"{Emojis.ARMOR} {player.user.display_name} {action_text} (+{armor_gain})"
        else:
            player.add_armor(armor_amount)
            self.last_action = f"{Emojis.ARMOR} {player.user.display_name} {action_text.replace('tăng giáp', f'tăng {armor_gain} giáp')}"
        
        self.switch_turn()
        await self.update_game(interaction)
    
    @discord.ui.button(label="🔮🛡️ Giáp Phép", style=discord.ButtonStyle.success, emoji="🔮")
    async def magic_armor(self, interaction: discord.Interaction, button: discord.ui.Button):
        player = self.current_turn
        
        # Check if player has enough energy
        if not player.use_energy(GameConstants.MAGIC_ARMOR_ENERGY):
            try:
                await interaction.response.send_message(f"❌ Không đủ Energy! (Cần {GameConstants.MAGIC_ARMOR_ENERGY} Energy)", ephemeral=True)
            except (discord.NotFound, discord.HTTPException):
                # Interaction expired, ignore
                pass
            return
        
        if player.restore_magic_armor():
            self.last_action = f"{Emojis.MAGIC_ARMOR} {player.user.display_name} khôi phục giáp phép!"
        else:
            # Return energy if already used
            player.energy += GameConstants.MAGIC_ARMOR_ENERGY
            self.last_action = f"❌ {player.user.display_name} đã sử dụng giáp phép rồi!"
        
        self.switch_turn()
        await self.update_game(interaction)
    
    @discord.ui.button(label="💊 Hồi máu", style=discord.ButtonStyle.success, emoji="💊")
    async def heal(self, interaction: discord.Interaction, button: discord.ui.Button):
        player = self.current_turn
        
        # Check if player has enough energy
        if not player.use_energy(GameConstants.HEAL_ENERGY):
            try:
                await interaction.response.send_message(f"❌ Không đủ Energy! (Cần {GameConstants.HEAL_ENERGY} Energy)", ephemeral=True)
            except (discord.NotFound, discord.HTTPException):
                # Interaction expired, ignore
                pass
            return
        
        # Check if player already has max HP
        if player.hp >= GameConstants.MAX_HP:
            try:
                await interaction.response.send_message("❌ HP đã đầy rồi!", ephemeral=True)
                # Return energy since heal was not used
                player.energy += GameConstants.HEAL_ENERGY
            except (discord.NotFound, discord.HTTPException):
                # Interaction expired, but still return energy
                player.energy += GameConstants.HEAL_ENERGY
            return
        
        heal_amount, action_text = GameLogic.calculate_heal_amount()
        actual_heal = player.heal(heal_amount)
        
        if actual_heal < heal_amount:
            # Adjusted action text for partial heal
            self.last_action = f"{Emojis.HEAL} {player.user.display_name} hồi {actual_heal} HP (tối đa)!"
        else:
            self.last_action = f"{Emojis.HEAL} {player.user.display_name} {action_text}"
        
        self.switch_turn()
        await self.update_game(interaction)

    @discord.ui.button(label="😴 Nghỉ ngơi", style=discord.ButtonStyle.secondary, emoji="😴")
    async def rest(self, interaction: discord.Interaction, button: discord.ui.Button):
        player = self.current_turn
        
        old_energy = player.energy
        player.rest()
        energy_gained = player.energy - old_energy
        
        self.last_action = f"{Emojis.REST} {player.user.display_name} nghỉ ngơi và hồi {energy_gained} Energy!"
        
        self.switch_turn()
        await self.update_game(interaction)
    
    @discord.ui.button(label="🏃 Trốn", style=discord.ButtonStyle.danger, emoji="🏃")
    async def run_away(self, interaction: discord.Interaction, button: discord.ui.Button):
        winner = self.player2 if self.current_turn == self.player1 else self.player1
        embed = GameLogic.create_run_away_embed(self.current_turn.user, winner)
        
        # Cancel AFK timer
        if self.afk_task:
            self.afk_task.cancel()
        
        # Disable all buttons
        self.clear_items()
        
        try:
            await interaction.response.edit_message(embed=embed, view=self)
        except (discord.NotFound, discord.HTTPException):
            # Interaction expired, ignore
            pass
    
    async def on_timeout(self):
        """Called when the view times out"""
        # Cancel AFK timer when view times out
        if self.afk_task:
            self.afk_task.cancel()
        
        # Mark game as over
        self.game_over = True


class ChallengeView(discord.ui.View):
    """Challenge acceptance view"""
    
    def __init__(self, challenger, opponent):
        super().__init__(timeout=GameConstants.CHALLENGE_TIMEOUT)
        self.challenger = challenger
        self.opponent = opponent
        self.result = None
        self._interaction: Optional[discord.Interaction] = None  # Store original interaction
    
    @discord.ui.button(label="Ýe, chơi luôn!", style=discord.ButtonStyle.success, emoji="⚔️")
    async def accept_challenge(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.opponent:
            await interaction.response.send_message("❌ Chỉ người được thách đấu mới có thể nhận!", ephemeral=True)
            return
        
        self.result = "accepted"
        
        # Start the game
        game_view = GameView(self.challenger, self.opponent)
        embed = GameLogic.create_game_embed(game_view.player1, game_view.player2, game_view.current_turn.user)
        
        await interaction.response.edit_message(embed=embed, view=game_view)
        
        # Store message reference for AFK system
        if hasattr(interaction, 'message') and interaction.message:
            game_view.current_message = interaction.message
    
    @discord.ui.button(label="Hong, sợ quá!", style=discord.ButtonStyle.danger, emoji="😰")
    async def decline_challenge(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.opponent:
            await interaction.response.send_message("❌ Chỉ người được thách đấu mới có thể từ chối!", ephemeral=True)
            return
        
        self.result = "declined"
        
        embed = discord.Embed(
            title=f"{Emojis.DECLINE} TỪ CHỐI THÁCH ĐẤU",
            description=f"**{self.opponent.display_name}** sợ quá nên biến rồi kkk 😂",
            color=EmbedColors.DECLINE
        )
        
        await interaction.response.edit_message(embed=embed, view=None)
    
    async def on_timeout(self):
        if self.result is None:
            embed = discord.Embed(
                title=f"{Emojis.TIMEOUT} HẾT THỜI GIAN",
                description=f"**{self.opponent.display_name}** sợ quá nên biến rồi kkk 😂",
                color=EmbedColors.TIMEOUT
            )
            
            # Clear all buttons
            self.clear_items()
            
            # Try to edit the message if we have the interaction
            if self._interaction:
                try:
                    await self._interaction.edit_original_response(embed=embed, view=self)
                except:
                    pass
