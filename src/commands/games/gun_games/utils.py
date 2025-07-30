"""
Các hàm tiện ích cho game Russian Roulette
"""
import discord
from typing import List, Optional
import re


def parse_players_from_string(players_str: str, guild: discord.Guild, host: discord.Member) -> List[discord.Member]:
    """
    Parse người chơi từ string mentions
    
    Args:
        players_str: String chứa mentions (@user1 @user2)
        guild: Discord guild
        host: Người tạo game
        
    Returns:
        List các discord.Member
    """
    members = []
    
    # Regex để tìm mentions
    mention_pattern = r'<@!?(\d+)>'
    matches = re.findall(mention_pattern, players_str)
    
    for user_id in matches:
        member = guild.get_member(int(user_id))
        if member and member not in members:
            members.append(member)
    
    # Thêm host nếu chưa có
    if host not in members:
        members.append(host)
    
    return members


def validate_player_count(members: List[discord.Member], min_players: int = 2, max_players: int = 8) -> tuple[bool, str]:
    """
    Kiểm tra số lượng người chơi
    
    Returns:
        (is_valid, error_message)
    """
    if len(members) < min_players:
        return False, f"🔫 Cần ít nhất {min_players} người chơi để bắt đầu!"
    
    if len(members) > max_players:
        return False, f"🔫 Tối đa {max_players} người chơi!"
    
    return True, ""


def create_player_list_text(members: List[discord.Member]) -> str:
    """Tạo text hiển thị danh sách người chơi"""
    return "\n".join([f"{i+1}. {member.mention}" for i, member in enumerate(members)])


def create_game_embed(gun_type, members: List[discord.Member], first_player: discord.Member) -> discord.Embed:
    """Tạo embed thông tin game"""
    embed = discord.Embed(
        title=f"🎮 Russian Roulette - {gun_type.name}",
        description=f"{gun_type.description}\n\n"
                   f"**Chambers:** {gun_type.chambers}\n"
                   f"**Đạn thật:** {gun_type.bullets}\n"
                   f"**Tỷ lệ sống:** {gun_type.survival_rate:.1f}%",
        color=discord.Color.red()
    )
    
    # Danh sách người chơi
    player_list = create_player_list_text(members)
    embed.add_field(name="👥 Người chơi", value=player_list, inline=False)
    
    # Người chơi đầu tiên
    embed.add_field(name="🎯 Lượt đầu tiên", value=first_player.mention, inline=True)
    
    embed.set_footer(text="Bấm vào chamber để bắn! Chúc may mắn! 🍀")
    
    return embed


def create_result_embed(current_player: discord.Member, chamber_id: int, chamber_result: str, 
                       gun_type, is_death: bool = False) -> discord.Embed:
    """Tạo embed kết quả sau khi bắn"""
    color = discord.Color.red() if is_death else discord.Color.green()
    embed = discord.Embed(color=color)
    
    if is_death:
        embed.title = f"💥 {current_player.display_name} đã bị loại!"
        embed.description = f"Chamber {chamber_id + 1} chứa đạn thật! {gun_type.emoji}"
        embed.set_thumbnail(url=current_player.display_avatar.url)
    else:
        embed.title = f"🔫 {current_player.display_name} an toàn!"
        embed.description = f"Chamber {chamber_id + 1} trống. Lượt tiếp theo!"
    
    return embed


def create_winner_embed(winner: Optional[discord.Member] = None) -> discord.Embed:
    """Tạo embed thông báo người thắng"""
    embed = discord.Embed(color=discord.Color.gold())
    
    if winner:
        embed.title = "🏆 Chúc mừng người chiến thắng!"
        embed.description = f"**{winner.display_name}** là người sống sót cuối cùng!"
        embed.set_thumbnail(url=winner.display_avatar.url)
        embed.add_field(
            name="🎉 Phần thưởng",
            value="Danh hiệu: **Người sống sót** 🏅",
            inline=False
        )
    else:
        embed.title = "💀 Không có người thắng"
        embed.description = "Tất cả đều đã bị loại!"
        embed.add_field(
            name="🪦 Kết quả",
            value="Trò chơi kết thúc mà không có người sống sót!",
            inline=False
        )
    
    return embed
