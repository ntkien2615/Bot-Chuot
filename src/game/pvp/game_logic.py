"""
Game logic for PvP battles
Handles combat calculations, turn management, and game state
"""

import random
import discord
from .player import Player
from .constants import DamageType, GameConstants, EmbedColors, Emojis


class GameLogic:
    """Handles game logic and combat calculations"""
    
    @staticmethod
    def calculate_punch_damage():
        """Calculate punch damage with critical hits and true damage"""
        base_damage = GameConstants.PUNCH_BASE_DAMAGE
        damage_type = DamageType.PHYSICAL
        
        # Check for critical hit
        crit_chance = random.randint(1, 100)
        crit_multiplier = 1.0
        crit_text = ""
        
        if crit_chance <= GameConstants.CRIT_CHANCE:
            crit_roll = random.randint(1, 100)
            for threshold, multiplier in GameConstants.CRIT_LEVELS.items():
                if crit_roll <= threshold:
                    crit_multiplier = multiplier
                    crit_text = f" (CRIT {int((multiplier-1)*100)}%!)"
                    break
        
        # Check for true damage
        true_damage_chance = random.randint(1, 100)
        if true_damage_chance <= GameConstants.TRUE_DAMAGE_CHANCE:
            damage_type = DamageType.TRUE
            
            # Check for true critical within true damage
            true_crit_chance = random.randint(1, 100)
            if true_crit_chance <= GameConstants.TRUE_CRIT_CHANCE:
                final_damage = GameConstants.TRUE_CRIT_DAMAGE
                action_text = f"gây {final_damage} sát thương chuẩn (CHÍ MẠNG CHUẨN!)!"
            else:
                final_damage = GameConstants.TRUE_DAMAGE_AMOUNT
                action_text = f"gây {final_damage} sát thương chuẩn!"
        else:
            final_damage = int(base_damage * crit_multiplier)
            action_text = f"gây {final_damage} sát thương vật lý{crit_text}!"
        
        return final_damage, damage_type, action_text
    
    @staticmethod
    def calculate_magic_damage(target):
        """Calculate magic damage and energy cost based on target state"""
        base_damage = GameConstants.MAGIC_BASE_DAMAGE
        energy_cost = GameConstants.MAGIC_ENERGY_BASE
        
        if target.magic_armor <= 0 and target.armor <= 0:
            # DEVASTATE mode: x2 damage and x2 energy cost
            final_damage = base_damage * 2
            energy_cost = GameConstants.MAGIC_ENERGY_DEVASTATE
            action_text = f"DEVASTATE: {final_damage} HP! (x2 energy: -{energy_cost})"
        else:
            final_damage = base_damage
            # Generate action text based on target state
            if target.magic_armor > 0:
                # Giáp phép sẽ hấp thụ hoàn toàn, không có damage thừa
                action_text = f"gây {final_damage} sát thương phép (HẤP THỤ HOÀN TOÀN)!"
            elif target.armor > 0:
                # Bào mòn: 50% damage lên giáp, 50% lên HP
                armor_damage = final_damage // 2
                hp_damage = final_damage - armor_damage
                action_text = f"BÀO MÒN: {armor_damage} giáp + {hp_damage} HP!"
        
        return final_damage, energy_cost, action_text
    
    @staticmethod
    def calculate_armor_gain():
        """Calculate armor gain with RNG"""
        chance = random.randint(1, 100)
        
        for threshold, (amount, text) in GameConstants.ARMOR_CHANCES.items():
            if chance <= threshold:
                return amount, text
        
        # Fallback (should not reach here)
        return 8, "tăng giáp!"
    
    @staticmethod
    def calculate_heal_amount():
        """Calculate heal amount with critical heal chance"""
        base_heal = GameConstants.HEAL_BASE_AMOUNT
        heal_multiplier = 1.0
        crit_text = ""
        
        # Check for critical heal
        crit_chance = random.randint(1, 100)
        if crit_chance <= GameConstants.HEAL_CRIT_CHANCE:
            crit_roll = random.randint(1, 100)
            for threshold, multiplier in GameConstants.HEAL_LEVELS.items():
                if crit_roll <= threshold:
                    heal_multiplier = multiplier
                    if multiplier == 2.0:
                        crit_text = " (HỒI TỐI ĐA!)"
                    else:
                        crit_text = f" (HIỆU QUẢ {int((multiplier-1)*100)}%!)"
                    break
        
        final_heal = int(base_heal * heal_multiplier)
        action_text = f"hồi {final_heal} HP{crit_text}!"
        
        return final_heal, action_text
    
    @staticmethod
    def create_game_embed(player1, player2, current_turn, last_action=""):
        """Create the main game embed"""
        embed = discord.Embed(
            title=f"{Emojis.CHALLENGE} TRẬN CHIẾN PVP {Emojis.CHALLENGE}",
            color=EmbedColors.GAME_PLAYER1 if current_turn == player1.user else EmbedColors.GAME_PLAYER2
        )
        
        # Thông tin Player 1
        embed.add_field(
            name=f"👤 {player1.user.display_name}",
            value=player1.get_status_text(),
            inline=True
        )
        
        # Thông tin Player 2
        embed.add_field(
            name=f"👤 {player2.user.display_name}",
            value=player2.get_status_text(),
            inline=True
        )
        
        embed.add_field(name="\u200b", value="\u200b", inline=False)
        
        if last_action:
            embed.add_field(name="📜 Hành động cuối:", value=last_action, inline=False)
        
        embed.add_field(name="🎯 Lượt của:", value=current_turn.display_name, inline=False)
        embed.add_field(
            name="💡 Chi phí Energy:", 
            value=f"{Emojis.PUNCH} Đấm: {GameConstants.PUNCH_ENERGY} | {Emojis.MAGIC} Phép: {GameConstants.MAGIC_ENERGY_BASE}/{GameConstants.MAGIC_ENERGY_DEVASTATE} | {Emojis.ARMOR} Giáp: {GameConstants.ARMOR_ENERGY} | {Emojis.MAGIC_ARMOR} Giáp Phép: {GameConstants.MAGIC_ARMOR_ENERGY} | {Emojis.HEAL} Hồi máu: {GameConstants.HEAL_ENERGY} | {Emojis.REST} Nghỉ: +{GameConstants.REST_ENERGY}", 
            inline=False
        )
        embed.add_field(
            name="⚖️ Cân bằng:", 
            value=f"🎲 Người đánh trước được chọn ngẫu nhiên\n🔋 Người bị đánh trước sẽ hồi energy ở turn đầu\n⏰ AFK quá {GameConstants.AFK_TIMEOUT}s = thua", 
            inline=False
        )
        embed.add_field(
            name=f"{Emojis.PUNCH} Đấm đặc biệt:", 
            value=f"{GameConstants.CRIT_CHANCE}% tỷ lệ CRIT (1.5x-2.5x damage)\n{GameConstants.TRUE_DAMAGE_CHANCE}% tỷ lệ True Damage ({GameConstants.TRUE_DAMAGE_AMOUNT} sát thương xuyên giáp)\n{GameConstants.TRUE_CRIT_CHANCE}% tỷ lệ CHÍ MẠNG CHUẨN ({GameConstants.TRUE_CRIT_DAMAGE} sát thương)", 
            inline=False
        )
        embed.add_field(
            name=f"{Emojis.MAGIC} Phép đặc biệt:", 
            value="Có giáp phép: HẤP THỤ (không overflow)\nCó giáp vật lý: BÀO MÒN (50% giáp + 50% HP)\nKhông giáp: DEVASTATE (x2 damage, x2 energy)", 
            inline=False
        )
        embed.add_field(
            name=f"{Emojis.HEAL} Hồi máu đặc biệt:", 
            value=f"{GameConstants.HEAL_CRIT_CHANCE}% tỷ lệ hồi hiệu quả (1.5x-2x heal)\nChi phí: {GameConstants.HEAL_ENERGY} Energy | Hồi cơ bản: {GameConstants.HEAL_BASE_AMOUNT} HP", 
            inline=False
        )
        
        return embed
    
    @staticmethod
    def create_victory_embed(winner, player1, player2):
        """Create victory embed"""
        embed = discord.Embed(
            title=f"{Emojis.VICTORY} KẾT THÚC TRẬN ĐẤU!",
            description=f"🎉 **{winner.user.display_name}** đã chiến thắng!",
            color=EmbedColors.VICTORY
        )
        embed.add_field(
            name="📊 Thống kê cuối trận:",
            value=(
                f"**{player1.user.display_name}:** {player1.hp} HP, {player1.armor} Giáp, {player1.energy} Energy\n"
                f"**{player2.user.display_name}:** {player2.hp} HP, {player2.armor} Giáp, {player2.energy} Energy"
            ),
            inline=False
        )
        return embed
    
    @staticmethod
    def create_run_away_embed(runner, winner):
        """Create run away embed"""
        embed = discord.Embed(
            title=f"{Emojis.RUN} TRỐN CHẠY!",
            description=f"💨 **{runner.display_name}** đã bỏ chạy khỏi trận đấu!",
            color=EmbedColors.RUN_AWAY
        )
        embed.add_field(
            name=f"{Emojis.VICTORY} Người chiến thắng:",
            value=f"🎉 **{winner.user.display_name}** thắng vì đối thủ bỏ cuộc!",
            inline=False
        )
        return embed
