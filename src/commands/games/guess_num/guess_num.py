import discord
from discord.ext import commands
from discord import app_commands
import random
import asyncio

from src.commands.base_command import GameCommand


class GuessNumCog(GameCommand):
    def __init__(self, discord_bot):
        super().__init__(discord_bot)
        # Store game data per channel
        self.game_data = {}  # {channel_id: {'number': int, 'guesses': int}}
    
    def start_game(self, channel_id):
        """Start a new game for the given channel"""
        self.game_data[channel_id] = {
            'number': random.randint(1, 100),
            'guesses': 0
        }
    
    def end_game(self, channel_id):
        """End the game for the given channel"""
        self.game_data.pop(channel_id, None)
    
    def is_game_active(self, channel_id):
        """Check if a game is active in the given channel"""
        return channel_id in self.game_data
    
    def check_win(self, channel_id, guess):
        """Check if the guess is correct, too low, or too high"""
        if channel_id not in self.game_data:
            return None
            
        game = self.game_data[channel_id]
        game['guesses'] += 1
        
        if guess == game['number']:
            return 'win'
        elif guess < game['number']:
            return 'low'
        else:
            return 'high'
    
    @app_commands.command(name='guess_num', description='Đoán số từ 1 đến 100')
    async def guess(self, interaction: discord.Interaction):
        # Ensure we have a valid text channel
        if not hasattr(interaction.channel, 'send') or interaction.channel is None:
            await interaction.response.send_message('Lệnh này chỉ có thể sử dụng trong text channel!', ephemeral=True)
            return
            
        channel_id = interaction.channel.id
        
        # Check if game is already in progress in this channel
        if self.is_game_active(channel_id):
            await interaction.response.send_message('Một trò chơi đã đang diễn ra trong kênh này!', ephemeral=True)
            return
        
        # Start new game
        self.start_game(channel_id)
        await interaction.response.send_message('🎯 **Đoán số từ 1 đến 100!**\nBạn có 20 giây để đoán. Hãy nhập một số!')

        try:
            def check(m):
                return m.author == interaction.user and m.channel == interaction.channel

            while self.is_game_active(channel_id):
                try:
                    message = await self.bot.wait_for('message', check=check, timeout=20.0)
                    
                    # Try to parse the guess
                    try:
                        guess = int(message.content)
                        if guess < 1 or guess > 100:
                            await message.reply('❌ Vui lòng đoán số từ 1 đến 100!')
                            continue
                            
                        # Check the guess
                        result = self.check_win(channel_id, guess)
                        if result == 'win':
                            game = self.game_data[channel_id]
                            await message.reply(f'🎉 **Chúc mừng!** Bạn đã đoán đúng số **{game["number"]}** sau **{game["guesses"]}** lần thử!')
                            self.end_game(channel_id)
                            break
                        elif result == 'low':
                            await message.add_reaction('🔼')
                            await message.reply('📈 Số bạn đoán **thấp** hơn! Thử số lớn hơn.')
                        elif result == 'high':
                            await message.add_reaction('🔽')
                            await message.reply('📉 Số bạn đoán **cao** hơn! Thử số nhỏ hơn.')
                        else:
                            # Game ended somehow
                            break
                            
                    except ValueError:
                        await message.reply('❌ Vui lòng nhập một **số** hợp lệ!')
                        
                except asyncio.TimeoutError:
                    if self.is_game_active(channel_id):
                        game = self.game_data[channel_id]
                        await interaction.followup.send(f'⏰ **Hết giờ!** Số cần đoán là **{game["number"]}**')
                        self.end_game(channel_id)
                    break

        except Exception as e:
            # Always clean up in case of errors
            self.end_game(channel_id)
            await interaction.followup.send('💥 Đã xảy ra lỗi trong trò chơi. Vui lòng thử lại!')
            print(f"Error in guess_num game: {e}")  # For debugging