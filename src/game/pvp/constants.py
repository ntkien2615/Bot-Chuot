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
    MAX_MAGIC_ARMOR = 20
    MAX_ENERGY = 100
    
    # Energy costs
    PUNCH_ENERGY = 20
    MAGIC_ENERGY_BASE = 40
    MAGIC_ENERGY_DEVASTATE = 80
    ARMOR_ENERGY = 30
    MAGIC_ARMOR_ENERGY = 45
    HEAL_ENERGY = 35
    
    # Energy regeneration
    ENERGY_REGEN = 20
    REST_ENERGY = 40
    
    # Combat values
    PUNCH_BASE_DAMAGE = 12
    MAGIC_BASE_DAMAGE = 15
    TRUE_DAMAGE_AMOUNT = 40
    TRUE_CRIT_DAMAGE = 60  # Sát thương chí mạng chuẩn
    HEAL_BASE_AMOUNT = 25
    
    # Probabilities (in percentage)
    CRIT_CHANCE = 40
    TRUE_DAMAGE_CHANCE = 15
    TRUE_CRIT_CHANCE = 5  # Tỷ lệ chí mạng chuẩn (trong số các True Damage)
    HEAL_CRIT_CHANCE = 20  # Tỷ lệ hồi máu tối đa
    
    # Crit multipliers
    CRIT_LEVELS = {
        30: 1.5,   # 30% of crit hits = 1.5x damage
        70: 2.0,   # 40% of crit hits = 2.0x damage  
        100: 2.5   # 30% of crit hits = 2.5x damage
    }
    
    # Heal multipliers  
    HEAL_LEVELS = {
        50: 1.5,   # 50% of heal crit = 1.5x heal
        100: 2.0   # 50% of heal crit = 2.0x heal (max heal)
    }
    
    # Armor gain probabilities
    ARMOR_CHANCES = {
        5: (50, "được full giáp!"),      # 5% chance for full armor
        15: (25, "tăng giáp! (May mắn!)"), # 10% chance for 25 armor
        35: (15, "tăng giáp!"),          # 20% chance for 15 armor
        100: (8, "tăng giáp!")           # 65% chance for 8 armor
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
