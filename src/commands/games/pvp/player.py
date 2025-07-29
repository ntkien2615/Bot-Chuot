"""
Player model for PvP game
Handles player stats, damage calculation, and actions
"""

from .constants import DamageType, GameConstants, Emojis


class Player:
    """Represents a player in the PvP game"""
    
    def __init__(self, user):
        self.user = user
        self.hp = GameConstants.MAX_HP
        self.armor = GameConstants.MAX_ARMOR
        self.magic_armor = GameConstants.MAX_MAGIC_ARMOR
        self.magic_armor_used = False
        self.energy = GameConstants.MAX_ENERGY
    
    def take_damage(self, damage, damage_type=DamageType.PHYSICAL):
        """
        Apply damage to player based on damage type
        
        Args:
            damage: Amount of damage to deal
            damage_type: DamageType enum value
        """
        if damage_type == DamageType.PHYSICAL:
            if self.armor > 0:
                self.armor -= damage
                if self.armor < 0:
                    self.hp += self.armor  # Trừ HP với phần damage thừa
                    self.armor = 0
            else:
                self.hp -= damage
                
        elif damage_type == DamageType.MAGIC:
            if self.magic_armor > 0:
                # Có giáp phép: HẤP THỤ HOÀN TOÀN - không có damage thừa
                # Dù sát thương phép lớn hơn giáp phép hiện tại, vẫn chỉ hấp thụ
                self.magic_armor = max(0, self.magic_armor - damage)
                # Không có damage thừa chảy sang HP
            else:
                # Không có giáp phép
                if self.armor > 0:
                    # Có giáp vật lý: BÀO MÒN - gây damage lên cả giáp và HP
                    armor_damage = damage // 2  # 50% damage lên giáp
                    hp_damage = damage - armor_damage  # 50% damage trực tiếp lên HP
                    
                    # Trừ giáp trước
                    self.armor -= armor_damage
                    if self.armor < 0:
                        self.armor = 0
                    
                    # Trừ HP trực tiếp (bào mòn)
                    self.hp -= hp_damage
                else:
                    # Không có cả giáp phép và giáp vật lý: DEVASTATE 
                    # (damage đã được tính x2 trong game_logic.py)
                    self.hp -= damage
                    
        elif damage_type == DamageType.TRUE:
            self.hp -= damage
        
        if self.hp < 0:
            self.hp = 0
    
    def add_armor(self, amount):
        """Add armor to player"""
        self.armor = min(GameConstants.MAX_ARMOR, self.armor + amount)
    
    def restore_magic_armor(self):
        """Restore magic armor if not used yet"""
        if not self.magic_armor_used:
            self.magic_armor = GameConstants.MAX_MAGIC_ARMOR
            self.magic_armor_used = True
            return True
        return False
    
    def use_energy(self, amount):
        """Use energy if available"""
        if self.energy >= amount:
            self.energy -= amount
            return True
        return False
    
    def regenerate_energy(self):
        """Regenerate energy"""
        self.energy = min(GameConstants.MAX_ENERGY, self.energy + GameConstants.ENERGY_REGEN)
    
    def rest(self):
        """Rest to regenerate energy"""
        self.energy = min(GameConstants.MAX_ENERGY, self.energy + GameConstants.REST_ENERGY)
    
    def heal(self, amount):
        """Heal HP"""
        old_hp = self.hp
        self.hp = min(GameConstants.MAX_HP, self.hp + amount)
        return self.hp - old_hp  # Trả về lượng HP thực sự được hồi
    
    def is_alive(self):
        """Check if player is alive"""
        return self.hp > 0
    
    def get_status_bars(self):
        """Get status bar representations"""
        hp_bar = Emojis.HP_BAR * (self.hp // 10) + Emojis.EMPTY_BAR * ((GameConstants.MAX_HP - self.hp) // 10)
        armor_bar = Emojis.ARMOR_BAR * (self.armor // 5) + Emojis.EMPTY_BAR * ((GameConstants.MAX_ARMOR - self.armor) // 5)
        magic_armor_bar = Emojis.MAGIC_ARMOR_BAR * (self.magic_armor // 3) + Emojis.EMPTY_BAR * ((GameConstants.MAX_MAGIC_ARMOR - self.magic_armor) // 3)  # Điều chỉnh cho MAX 15
        energy_bar = Emojis.ENERGY_BAR * (self.energy // 10) + Emojis.EMPTY_BAR * ((GameConstants.MAX_ENERGY - self.energy) // 10)
        
        return {
            'hp_bar': hp_bar,
            'armor_bar': armor_bar,
            'magic_armor_bar': magic_armor_bar,
            'energy_bar': energy_bar
        }
    
    def get_status_text(self):
        """Get formatted status text"""
        bars = self.get_status_bars()
        return (
            f"❤️ HP: {self.hp}/{GameConstants.MAX_HP}\n{bars['hp_bar']}\n"
            f"🛡️ Giáp: {self.armor}/{GameConstants.MAX_ARMOR}\n{bars['armor_bar']}\n"
            f"🔮 Giáp phép: {self.magic_armor}/{GameConstants.MAX_MAGIC_ARMOR}\n{bars['magic_armor_bar']}\n"
            f"⚡ Energy: {self.energy}/{GameConstants.MAX_ENERGY}\n{bars['energy_bar']}"
        )
