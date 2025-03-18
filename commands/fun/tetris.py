import discord
from discord.ext import commands
from discord import app_commands
import random
import asyncio

# Constants
NUM_OF_ROWS = 18
NUM_OF_COLS = 10
EMPTY_SQUARE = ':black_large_square:'
SQUARES = {
    'blue': ':blue_square:',
    'brown': ':brown_square:',
    'orange': ':orange_square:',
    'yellow': ':yellow_square:',
    'green': ':green_square:',
    'purple': ':purple_square:',
    'red': ':red_square:'
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
            await asyncio.sleep(1)
        else:
            await asyncio.sleep(0.1)
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

class TetrisSlash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = bot  # Add client reference
        self.active_games = {}  # Track active games

    @app_commands.command(name='tetris', description='chơi tetris với bot')
    async def tetrisSlash(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await reset_game()
        embed = discord.Embed(description=format_board_as_str(), color=EMBED_COLOUR)
        msg = await interaction.followup.send(embed=embed)
        for emoji in ["⬅", "⬇", "➡", "🔃"]:
            await msg.add_reaction(emoji)
        cur_shape = get_random_shape()
        await run_game(msg, cur_shape, interaction)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot or not hasattr(reaction.message, 'author') or reaction.message.author.id != self.bot.user.id:
            return

        try:
            global h_movement, down_pressed, rotate_clockwise, rotation_pos
            if reaction.emoji == "⬅":
                h_movement = -1
            elif reaction.emoji == "➡":
                h_movement = 1
            elif reaction.emoji == "⬇":
                down_pressed = True
                await asyncio.sleep(0.3)  # Allow time for the shape to move down
                down_pressed = False  # Reset down_pressed after processing
            elif reaction.emoji == "🔃":
                rotate_clockwise = True
                rotation_pos = (rotation_pos + 1) % 4  # Update rotation position
            
            await reaction.message.remove_reaction(reaction.emoji, user)
        except Exception as e:
            print(f"Error handling reaction: {e}")

async def setup(bot):
    await bot.add_cog(TetrisSlash(bot))