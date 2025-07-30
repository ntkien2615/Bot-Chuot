"""
Russian Roulette Game Package

Cấu trúc:
- gun_types.py: Định nghĩa các loại súng
- utils.py: Các hàm tiện ích
- gun_game_view.py: UI và logic game
- gun_roulette.py: Command chính

Cách sử dụng:
/gun_roulette - Tạo room mời người chơi
/gun_quick @user1 @user2 - Chơi nhanh với người được mention
"""

from .gun_roulette import GunRoulette

__all__ = ['GunRoulette']
