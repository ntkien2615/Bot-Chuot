"""
Constants and enums for PvP game
Defines game constants, damage types, and other enumerations
"""

from enum import Enum


class DamageType(Enum):
    """Types of damage in PvP"""
    PHYSICAL = "physical"
    MAGIC = "magic"
    TRUE = "true"


class ActionType(Enum):
    """Types of actions players can take"""
    PUNCH = "punch"
    MAGIC = "magic" 
    ARMOR = "armor"
    MAGIC_ARMOR = "magic_armor"
    HEAL = "heal"
    REST = "rest"
    RUN = "run"


class GameConstants:
    """Game balance constants"""
    
    # Player stats
    MAX_HP = 100
    MAX_ARMOR = 50
    MAX_MAGIC_ARMOR = 15  # Giảm từ 20 xuống 15 để cân bằng
    MAX_ENERGY = 100
    
    # Energy costs
    PUNCH_ENERGY = 20
    MAGIC_ENERGY_BASE = 40
    MAGIC_ENERGY_DEVASTATE = 80
    ARMOR_ENERGY = 30
    MAGIC_ARMOR_ENERGY = 50  # Tăng từ 45 lên 50 để cân bằng chi phí
    HEAL_ENERGY = 35  # Tăng từ 30 lên 35 để hạn chế heal spam
    
    # Energy regeneration
    ENERGY_REGEN = 20
    REST_ENERGY = 40
    
    # Combat values
    PUNCH_BASE_DAMAGE = 12
    MAGIC_BASE_DAMAGE = 15
    TRUE_DAMAGE_AMOUNT = 40
    TRUE_CRIT_DAMAGE = 60  # Sát thương chí mạng chuẩn
    HEAL_BASE_AMOUNT = 20  # Giảm từ 30 xuống 20 để tránh heal spam
    
    # Probabilities (in percentage)
    CRIT_CHANCE = 40
    TRUE_DAMAGE_CHANCE = 15
    TRUE_CRIT_CHANCE = 5  # Tỷ lệ chí mạng chuẩn (trong số các True Damage)
    HEAL_CRIT_CHANCE = 15  # Giảm từ 25% xuống 15% để hạn chế crit heal
    
    # Crit multipliers
    CRIT_LEVELS = {
        30: 1.5,   # 30% of crit hits = 1.5x damage
        70: 2.0,   # 40% of crit hits = 2.0x damage  
        100: 2.5   # 30% of crit hits = 2.5x damage
    }
    
    # Heal multipliers - Nerf để tránh heal quá mạnh
    HEAL_LEVELS = {
        50: 1.3,   # Giảm từ 1.5x xuống 1.3x và tăng ngưỡng từ 40% lên 50%
        100: 1.6   # Giảm từ 2.0x xuống 1.6x để hạn chế heal spam
    }
    
    # Armor gain probabilities - Cân bằng lại để giảm RNG
    ARMOR_CHANCES = {
        8: (40, "được full giáp!"),      # Tăng từ 5% lên 8% 
        20: (25, "tăng giáp! (May mắn!)"), # Tăng từ 15% lên 20%
        45: (18, "tăng giáp!"),          # Tăng từ 35% lên 45% và tăng lượng giáp
        100: (12, "tăng giáp!")          # Tăng lượng giáp từ 8 lên 12
    }
    
    # Timeouts
    GAME_TIMEOUT = 60.0
    CHALLENGE_TIMEOUT = 20.0
    AFK_TIMEOUT = 20.0  # Thời gian AFK tối đa (giây)


class EmbedColors:
    """Colors for different embed types"""
    GAME_PLAYER1 = 0xff6b6b
    GAME_PLAYER2 = 0x4ecdc4
    VICTORY = 0xffd700
    RUN_AWAY = 0x95a5a6
    CHALLENGE = 0xff9800
    DECLINE = 0x95a5a6
    TIMEOUT = 0x95a5a6


class Emojis:
    """Emojis used in the game"""
    
    # Status bars
    HP_BAR = "🟥"
    ARMOR_BAR = "🟦"
    MAGIC_ARMOR_BAR = "🟪"
    ENERGY_BAR = "🟨"
    EMPTY_BAR = "⬛"
    
    # Actions
    PUNCH = "👊"
    MAGIC = "🔮"
    ARMOR = "🛡️"
    MAGIC_ARMOR = "🔮🛡️"
    HEAL = "💊"
    REST = "😴"
    RUN = "🏃"
    
    # Game states
    VICTORY = "🏆"
    CHALLENGE = "⚔️"
    DECLINE = "😰"
    TIMEOUT = "⏰"
