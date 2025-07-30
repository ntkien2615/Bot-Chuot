"""
Định nghĩa các loại súng khác nhau cho game Russian Roulette
"""
from typing import Optional


class GunType:
    """Định nghĩa thông tin của một loại súng"""
    def __init__(self, name: str, description: str, chambers: int, bullets: int, emoji: str, special_ability: Optional[str] = None):
        self.name = name
        self.description = description
        self.chambers = chambers  # Số viên đạn tổng
        self.bullets = bullets    # Số viên đạn thật
        self.emoji = emoji
        self.special_ability = special_ability
        
    @property
    def survival_rate(self) -> float:
        """Tính tỷ lệ sống sót"""
        return ((self.chambers - self.bullets) / self.chambers) * 100
    
    def __str__(self):
        return f"{self.emoji} {self.name} ({self.chambers} viên, {self.bullets} đạn thật)"


# Định nghĩa tất cả các loại súng
GUN_TYPES = {
    "revolver": GunType(
        name="Classic Revolver",
        description="Súng lục kinh điển 6 viên - trò chơi cổ điển",
        chambers=6,
        bullets=1,
        emoji="🔫"
    ),
    "shotgun": GunType(
        name="Shotgun Roulette",
        description="Súng hoa cải 2 nòng - nhanh gọn lẹ",
        chambers=2,
        bullets=1,
        emoji="💥"
    ),
    "sniper": GunType(
        name="Sniper Precision",
        description="Súng bắn tỉa 5 viên - cần sự chính xác",
        chambers=5,
        bullets=1,
        emoji="🎯"
    ),
    "machine": GunType(
        name="Machine Gun",
        description="Súng máy 8 viên - nhiều đạn hơn",
        chambers=8,
        bullets=2,
        emoji="🔥"
    ),
    "extreme": GunType(
        name="Extreme Roulette",
        description="Chế độ cực khó 6 viên - rất nguy hiểm",
        chambers=6,
        bullets=3,
        emoji="☠️"
    ),
    "lucky": GunType(
        name="Lucky Seven",
        description="May mắn số 7 - thử vận may",
        chambers=7,
        bullets=1,
        emoji="🍀"
    ),
    "double": GunType(
        name="Double Barrel",
        description="Súng 2 nòng nguy hiểm - rủi ro cao",
        chambers=4,
        bullets=2,
        emoji="⚡"
    ),
    "russian": GunType(
        name="True Russian",
        description="Phiên bản Nga chính thống 6 viên",
        chambers=6,
        bullets=2,
        emoji="🇷🇺"
    ),
    "wild": GunType(
        name="Wild West",
        description="Miền Tây hoang dã 8 viên",
        chambers=8,
        bullets=3,
        emoji="🤠"
    ),
    "tactical": GunType(
        name="Tactical Ops",
        description="Chiến thuật quân sự 10 viên",
        chambers=10,
        bullets=2,
        emoji="🎖️"
    )
}


def get_gun_type(gun_key: str) -> Optional[GunType]:
    """Lấy thông tin súng theo key"""
    return GUN_TYPES.get(gun_key)


def get_all_gun_choices():
    """Lấy danh sách choices cho Discord command"""
    from discord import app_commands
    
    choices = []
    for key, gun in GUN_TYPES.items():
        choice_name = f"{gun.emoji} {gun.name} ({gun.chambers} viên, {gun.bullets} đạn)"
        if len(choice_name) > 100:  # Discord limit
            choice_name = f"{gun.emoji} {gun.name}"
        choices.append(app_commands.Choice(name=choice_name, value=key))
    
    return choices
