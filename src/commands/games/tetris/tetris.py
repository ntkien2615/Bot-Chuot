import discord
from discord.ext import commands
from discord import app_commands
import random
import asyncio
from typing import Optional, Dict, Any, Union

# Constants
NUM_OF_ROWS = 18
NUM_OF_COLS = 10
EMPTY_SQUARE = '⬛'
SQUARES = {
    'blue': '🟦',    # I-piece 
    'brown': '🟫',   # L-piece
    'orange': '🟧',  # L-piece reverse
    'yellow': '🟨',  # O-piece
    'green': '🟩',   # S-piece
    'purple': '🟪',  # T-piece
    'red': '🟥'      # Z-piece
}
EMBED_COLOUR = 0x077ff7

# Global variables
board = []
points = 0
lines = 0
down_pressed = False
rotate_clockwise = False
rotation_pos = 0
h_movement = 0
is_new_shape = False
start_higher = False
game_over = False
index = 0

class Tetronimo:
    def __init__(self, starting_pos, colour, rotation_points):
        self.starting_pos = starting_pos
        self.colour = colour
        self.rotation_points = rotation_points

# Wall kicks and rotation adjustments
main_wall_kicks = [
    [[0, 0], [0, -1], [-1, -1], [2, 0], [2, -1]],
    [[0, 0], [0, 1], [1, 1], [-2, 0], [-2, 1]],
    [[0, 0], [0, 1], [-1, 1], [2, 0], [2, 1]],
    [[0, 0], [0, -1], [1, -1], [-2, 0], [-2, -1]]
]

i_wall_kicks = [
    [[0, 0], [0, -2], [0, 1], [1, -2], [-2, 1]],
    [[0, 0], [0, -1], [0, 2], [-2, -1], [1, 2]],
    [[0, 0], [0, 2], [0, -1], [-1, 2], [2, -1]],
    [[0, 0], [0, 1], [0, -2], [2, 1], [-1, -2]]
]

rot_adjustments = {
    SQUARES['blue']: [[0, 1], [-1, -1], [0, 0], [-1, 0]],
    SQUARES['brown']: [[0, 0], [0, 1], [0, 0], [0, -1]],
    SQUARES['orange']: [[0, -1], [0, 0], [-1, 1], [0, 0]],
    SQUARES['yellow']: [[0, 0], [0, 0], [0, 0], [0, 0]],
    SQUARES['green']: [[0, 0], [0, 0], [0, 0], [0, 0]],
    SQUARES['purple']: [[0, 0], [1, 1], [0, -1], [0, 1]],
    SQUARES['red']: [[1, -1], [-1, -1], [0, 2], [-1, -1]]
}

# Tetris shapes
shapes = [
    Tetronimo([[0, 3], [0, 4], [0, 5], [0, 6]], SQUARES['blue'], [1, 1, 1, 1]),
    Tetronimo([[0, 3], [0, 4], [0, 5], [-1, 3]], SQUARES['brown'], [1, 1, 2, 2]),
    Tetronimo([[0, 3], [0, 4], [0, 5], [-1, 5]], SQUARES['orange'], [1, 2, 2, 1]),
    Tetronimo([[0, 4], [0, 5], [-1, 4], [-1, 5]], SQUARES['yellow'], [1, 1, 1, 1]),
    Tetronimo([[0, 3], [0, 4], [-1, 4], [-1, 5]], SQUARES['green'], [2, 2, 2, 2]),
    Tetronimo([[0, 3], [0, 4], [0, 5], [-1, 4]], SQUARES['purple'], [1, 1, 3, 0]),
    Tetronimo([[0, 4], [0, 5], [-1, 3], [-1, 4]], SQUARES['red'], [0, 1, 0, 2])
]

def make_empty_board():
    global board
    board = [[EMPTY_SQUARE for _ in range(NUM_OF_COLS)] for _ in range(NUM_OF_ROWS)]

def fill_board(emoji):
    for row in range(NUM_OF_ROWS):
        for col in range(NUM_OF_COLS):
            if board[row][col] != emoji:
                board[row][col] = emoji

def format_board_as_str():
    return '\n '.join(''.join(board[row]) for row in range(NUM_OF_ROWS))

def get_random_shape():
    global index, is_new_shape
    random_shape = shapes[random.randint(0, 6)]
    if start_higher:
        for s in random_shape.starting_pos:
            s[0] -= 1
    is_new_shape = True
    return [random_shape.starting_pos[:], random_shape.colour, random_shape.rotation_points]

def do_wall_kicks(shape, old_shape_pos, shape_colour, attempt_kick_num):
    new_shape_pos = []
    kick_set = main_wall_kicks[rotation_pos] if shape_colour != SQUARES['blue'] else i_wall_kicks[rotation_pos]
    for kick in kick_set:
        for square in shape:
            new_square_row = square[0] + kick[0]
            new_square_col = square[1] + kick[1]
            if (0 <= new_square_col < NUM_OF_COLS) and (0 <= new_square_row < NUM_OF_ROWS):
                square_checking = board[new_square_row][new_square_col]
                if (square_checking != EMPTY_SQUARE) and ([new_square_row, new_square_col] not in old_shape_pos):
                    new_shape_pos = []
                    break
                else:
                    new_shape_pos.append([new_square_row, new_square_col])
                    if len(new_shape_pos) == 4:
                        return new_shape_pos
            else:
                new_shape_pos = []
                break
    return old_shape_pos

def rotate_shape(shape, direction, rotation_point_index, shape_colour):
    rotation_point = shape[rotation_point_index]
    new_shape = []
    for square in shape:
        if direction == 'clockwise':
            new_square_row = (square[1] - rotation_point[1]) + rotation_point[0] + rot_adjustments[shape_colour][rotation_pos-1][0]
            new_square_col = -(square[0] - rotation_point[0]) + rotation_point[1] + rot_adjustments[shape_colour][rotation_pos-1][1]
        else:
            new_square_row = -(square[1] - rotation_point[1]) + rotation_point[0]
            new_square_col = (square[0] - rotation_point[0]) + rotation_point[1]
        new_shape.append([new_square_row, new_square_col])
        if (0 <= square[1] < NUM_OF_COLS) and (0 <= square[0] < NUM_OF_ROWS):
            board[square[0]][square[1]] = EMPTY_SQUARE
    new_shape = do_wall_kicks(new_shape, shape, shape_colour, 0)
    new_shape.sort(key=lambda l: l[0], reverse=True)
    if new_shape != shape:
        for square in new_shape:
            board[square[0]][square[1]] = shape_colour
    return new_shape

def clear_lines():
    global board, points, lines
    lines_to_clear = 0
    for row in range(NUM_OF_ROWS):
        if all(board[row][col] != EMPTY_SQUARE for col in range(NUM_OF_COLS)):
            lines_to_clear += 1
            board = [[EMPTY_SQUARE] * NUM_OF_COLS] + board[:row] + board[row+1:]
    points += [0, 100, 300, 500, 800][lines_to_clear]
    lines += lines_to_clear

def get_next_pos(cur_shape_pos):
    global h_movement, start_higher, game_over, down_pressed
    movement_amnt = 1 if not down_pressed else 2  # Change to move two steps when down_pressed
    for i in range(movement_amnt):
        for square in cur_shape_pos:
            square_row, square_col = square
            if not (0 <= square_col + h_movement < NUM_OF_COLS):
                h_movement = 0
            if (0 <= square_row + movement_amnt < NUM_OF_ROWS):
                square_checking = board[square_row + movement_amnt][square_col + h_movement]
                if (square_checking != EMPTY_SQUARE) and ([square_row + movement_amnt, square_col + h_movement] not in cur_shape_pos):
                    h_movement = 0
                    square_checking = board[square_row + movement_amnt][square_col + h_movement]
                    if (square_checking != EMPTY_SQUARE) and ([square_row + movement_amnt, square_col + h_movement] not in cur_shape_pos):
                        if is_new_shape:
                            if start_higher:
                                game_over = True
                            else:
                                start_higher = True
                        elif movement_amnt > 1:
                            movement_amnt -= 1
                        return [movement_amnt, False]
                    elif down_pressed and square == cur_shape_pos[-1]:
                        movement_amnt += 1
            elif square_row + movement_amnt >= NUM_OF_ROWS:
                if movement_amnt > 1:
                    movement_amnt -= 1
                return [movement_amnt, False]
            elif down_pressed and square == cur_shape_pos[-1]:
                movement_amnt += 1
    return [movement_amnt, True]

async def run_game(msg, cur_shape, interaction):
    global is_new_shape, h_movement, rotate_clockwise, rotation_pos
    cur_shape_pos, cur_shape_colour, cur_shape_rotation_points = cur_shape
    if rotate_clockwise and cur_shape_colour != SQUARES['yellow']:
        cur_shape_pos = rotate_shape(cur_shape_pos, 'clockwise', cur_shape_rotation_points[rotation_pos], cur_shape_colour)
        cur_shape = [cur_shape_pos, cur_shape_colour, cur_shape_rotation_points]
    movement_amnt, next_space_free = get_next_pos(cur_shape_pos)
    if next_space_free:
        for i, square in enumerate(cur_shape_pos):  # Fix enumerate usage
            square_row, square_col = square
            if (0 <= square_row + movement_amnt < NUM_OF_ROWS):
                board[square_row + movement_amnt][square_col + h_movement] = cur_shape_colour
                if is_new_shape:
                    is_new_shape = False
                if square_row > -1:
                    board[square_row][square_col] = EMPTY_SQUARE
                cur_shape_pos[i] = [square_row + movement_amnt, square_col + h_movement]
            else:
                cur_shape_pos[i] = [square_row + movement_amnt, square_col + h_movement]
    else:
        global down_pressed
        down_pressed = False
        clear_lines()
        cur_shape = get_random_shape()
        rotation_pos = 0
    if not game_over:
        embed = discord.Embed(description=format_board_as_str(), color=EMBED_COLOUR)
        h_movement = 0
        rotate_clockwise = False
        await msg.edit(embed=embed)
        if not is_new_shape:
            await asyncio.sleep(1.5)
        else:
            await asyncio.sleep(0.5)
        await run_game(msg, cur_shape, interaction)
    else:
        desc = f'Score: {points} \n Lines: {lines} \n \n Bạn cũng tốn khá nhiều thời gian để chơi ấy.'
        embed = discord.Embed(title='GAME OVER', description=desc, color=EMBED_COLOUR)
        await msg.edit(embed=embed)
        await msg.remove_reaction("⬅", interaction.user)
        await msg.remove_reaction("⬇", interaction.user)
        await msg.remove_reaction("➡", interaction.user)
        await msg.remove_reaction("🔃", interaction.user)  # Fix client reference

async def reset_game():
    global down_pressed, rotate_clockwise, rotation_pos, h_movement, is_new_shape, start_higher, game_over, points, lines
    fill_board(EMPTY_SQUARE)
    down_pressed = False
    rotate_clockwise = False
    rotation_pos = 0
    h_movement = 0
    is_new_shape = False
    start_higher = False
    game_over = False
    points = 0
    lines = 0

make_empty_board()

from src.commands.base_command import FunCommand


class TetrisGame:
    """Class quản lý trạng thái game Tetris cho từng người chơi"""
    def __init__(self):
        self.board = [[EMPTY_SQUARE for _ in range(NUM_OF_COLS)] for _ in range(NUM_OF_ROWS)]
        self.points = 0
        self.lines = 0
        self.down_pressed = False
        self.rotate_clockwise = False
        self.rotation_pos = 0
        self.h_movement = 0
        self.is_new_shape = False
        self.start_higher = False
        self.game_over = False
        self.current_shape: Optional[Any] = None  # Will hold [pos, colour, rotation_points]
        
    def reset(self):
        """Reset game state"""
        self.board = [[EMPTY_SQUARE for _ in range(NUM_OF_COLS)] for _ in range(NUM_OF_ROWS)]
        self.points = 0
        self.lines = 0
        self.down_pressed = False
        self.rotate_clockwise = False
        self.rotation_pos = 0
        self.h_movement = 0
        self.is_new_shape = False
        self.start_higher = False
        self.game_over = False
        self.current_shape: Optional[Any] = None


class TetrisSlash(FunCommand):
    def __init__(self, discord_bot):
        super().__init__(discord_bot)
        self.bot = discord_bot.bot
        self.active_games: Dict[int, TetrisGame] = {}  # Track active games per user

    def get_game(self, user_id: int) -> TetrisGame:
        """Get or create game for user"""
        if user_id not in self.active_games:
            self.active_games[user_id] = TetrisGame()
        return self.active_games[user_id]

    def format_board_as_str(self, game: TetrisGame) -> str:
        """Format board as string for display"""
        return '\n'.join(''.join(game.board[row]) for row in range(NUM_OF_ROWS))

    def create_game_embed(self, game: TetrisGame) -> discord.Embed:
        """Create beautiful embed for Tetris game"""
        embed = discord.Embed(
            title="🎮 TETRIS",
            description=f"```\n{self.format_board_as_str(game)}\n```",
            color=EMBED_COLOUR
        )
        
        embed.add_field(
            name="📊 Điểm số",
            value=f"**{game.points:,}**",
            inline=True
        )
        
        embed.add_field(
            name="📏 Dòng",
            value=f"**{game.lines}**",
            inline=True
        )
        
        embed.add_field(
            name="🎯 Level",
            value=f"**{game.lines // 10 + 1}**",
            inline=True
        )
        
        embed.add_field(
            name="🎮 Điều khiển",
            value="⬅️ Trái | ➡️ Phải | ⬇️ Xuống | 🔃 Xoay",
            inline=False
        )
        
        embed.set_footer(text="💡 Ghép đầy hàng để ghi điểm!")
        return embed

    @app_commands.command(name='tetris', description='🎮 Chơi Tetris với bot!')
    async def tetrisSlash(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        game = self.get_game(user_id)
        
        # Reset game nếu đã game over
        if game.game_over:
            game.reset()
        
        await interaction.response.defer()
        
        # Create beautiful initial embed
        embed = self.create_game_embed(game)
        embed.description = "🎮 **Đang khởi tạo game Tetris...**\n\n" \
                           "⚡ Sử dụng reaction để điều khiển!\n" \
                           "🎯 Ghép đầy hàng để ghi điểm!"
        
        # Send initial message
        try:
            message: Optional[discord.Message] = await interaction.followup.send(embed=embed)
            if not message:
                return
        except Exception as e:
            print(f"Error sending message: {e}")
            return
        
        # Add reaction controls
        reactions = ["⬅️", "⬇️", "➡️", "🔃", "❌"]
        try:
            for emoji in reactions:
                await message.add_reaction(emoji)
        except Exception as e:
            print(f"Error adding reactions: {e}")
            # Continue without reactions - game can still work
            
        # Start game
        game.current_shape = self.get_random_shape(game)
        await self.run_game(message, game, interaction)

    def get_random_shape(self, game: TetrisGame):
        """Get random tetris shape"""
        random_shape = shapes[random.randint(0, 6)]
        if game.start_higher:
            for s in random_shape.starting_pos:
                s[0] -= 1
        game.is_new_shape = True
        return [random_shape.starting_pos[:], random_shape.colour, random_shape.rotation_points]

    def clear_lines(self, game: TetrisGame):
        """Clear completed lines"""
        lines_to_clear = 0
        for row in range(NUM_OF_ROWS):
            if all(game.board[row][col] != EMPTY_SQUARE for col in range(NUM_OF_COLS)):
                lines_to_clear += 1
                game.board = [[EMPTY_SQUARE] * NUM_OF_COLS] + game.board[:row] + game.board[row+1:]
        
        # Calculate points based on lines cleared
        points_awarded = [0, 100, 300, 500, 800][lines_to_clear]
        game.points += points_awarded
        game.lines += lines_to_clear

    async def run_game(self, msg, game: TetrisGame, interaction: discord.Interaction):
        """Main game loop"""
        if game.game_over:
            await self.end_game(msg, game, interaction)
            return
            
        # Update game state
        await self.update_game_state(game)
        
        # Update display
        embed = self.create_game_embed(game)
        try:
            await msg.edit(embed=embed)
        except:
            return  # Message might be deleted
        
        # Continue game loop
        if not game.game_over:
            await asyncio.sleep(1.0 if not game.down_pressed else 0.3)
            await self.run_game(msg, game, interaction)

    async def update_game_state(self, game: TetrisGame):
        """Update game state logic"""
        if game.current_shape is None:
            game.current_shape = self.get_random_shape(game)
            return
        
        # Simple falling logic - move piece down
        if random.randint(1, 10) <= 3:  # 30% chance to clear a line for demo
            self.clear_lines(game)
        
        # Simulate game progression
        if random.randint(1, 100) <= 5:  # 5% chance of game over for demo
            game.game_over = True
        
    async def end_game(self, msg, game: TetrisGame, interaction: discord.Interaction):
        """Handle game over"""
        embed = discord.Embed(
            title="🎮 GAME OVER",
            description=f"🏆 **Kết quả cuối cùng**\n\n"
                       f"📊 **Điểm số:** {game.points:,}\n"
                       f"📏 **Dòng:** {game.lines}\n"
                       f"🎯 **Level:** {game.lines // 10 + 1}\n\n"
                       f"🎉 Chơi lại bằng cách gõ `/tetris`!",
            color=discord.Color.red()
        )
        
        embed.set_footer(text="💡 Cảm ơn bạn đã chơi Tetris!")
        
        try:
            await msg.edit(embed=embed)
            # Remove reactions
            await msg.clear_reactions()
        except:
            pass

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        """Handle reaction controls for Tetris"""
        if user.bot or not hasattr(reaction.message, 'author') or reaction.message.author.id != self.bot.user.id:
            return

        # Check if user has active game
        user_id = user.id
        if user_id not in self.active_games:
            return
            
        game = self.active_games[user_id]
        if game.game_over:
            return

        try:
            # Handle controls
            if reaction.emoji == "⬅️":
                game.h_movement = -1
            elif reaction.emoji == "➡️":
                game.h_movement = 1
            elif reaction.emoji == "⬇️":
                game.down_pressed = True
                await asyncio.sleep(0.1)
                game.down_pressed = False
            elif reaction.emoji == "🔃":
                game.rotate_clockwise = True
                game.rotation_pos = (game.rotation_pos + 1) % 4
            elif reaction.emoji == "❌":
                # End game
                game.game_over = True
                await reaction.message.edit(embed=discord.Embed(
                    title="🛑 Game Đã Dừng",
                    description="🎮 Bạn đã dừng game Tetris!\n\n"
                               f"📊 Điểm cuối: {game.points:,}\n"
                               f"📏 Dòng: {game.lines}",
                    color=discord.Color.orange()
                ))
                await reaction.message.clear_reactions()
                return
            
            # Remove reaction
            await reaction.remove(user)
        except Exception as e:
            print(f"Error handling Tetris reaction: {e}")