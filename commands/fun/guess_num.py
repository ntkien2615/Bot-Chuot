import discord
from discord.ext import commands
from discord import app_commands
import random
import asyncio

class GuessNumCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.number = random.randint(1, 100)
        self.guesses = 0
        self.game_in_progress = {}  # Track games by channel
    
    def reset_data(self, channel_id):
        self.number = self.random_number()
        self.guesses = 0
        self.game_in_progress.pop(channel_id, None)
    
    def random_number(self):
        return random.randint(1, 100)
    
    def check_win(self, guess):
        if guess == self.number:
            return 'win'
        elif guess < self.number:
            return 'low'
        else:
            return 'high'
    
    @app_commands.command(name = 'guess_num', description='Đoán số')
    async def guess(self, interaction: discord.Interaction):
        channel_id = interaction.channel.id
        if channel_id in self.game_in_progress:
            await interaction.response.send_message('Một trò chơi đã đang diễn ra trong kênh này!', ephemeral=True)
            return
            
        self.game_in_progress[channel_id] = True
        self.reset_data(channel_id)
        await interaction.response.send_message('Đoán số từ 1 đến 100')

        try:
            def check(m):
                return m.author == interaction.user and m.channel == interaction.channel

            while True:
                try:
                    message = await self.bot.wait_for('message', check=check, timeout=20.0)
                    try:
                        guess = int(message.content)
                        if guess < 1 or guess > 100:
                            await interaction.channel.send(f'{message.author.mention}, vui lòng đoán số từ 1 đến 100')
                            continue
                            
                        result = self.check_win(guess)
                        if result == 'win':
                            await interaction.channel.send(f'Chúc mừng {message.author.mention}, bạn đã đoán đúng số {self.number}!')
                            self.reset_data(channel_id)
                            break
                        elif result == 'low':
                            await interaction.channel.send(f'{message.author.mention}, số bạn đoán nhỏ hơn số cần đoán')
                        else:
                            await interaction.channel.send(f'{message.author.mention}, số bạn đoán lớn hơn số cần đoán')
                    except ValueError:
                        await interaction.channel.send(f'{message.author.mention}, vui lòng nhập một số hợp lệ')
                        
                except asyncio.TimeoutError:
                    await interaction.channel.send(f'Hết giờ! Số cần đoán là {self.number}')
                    self.reset_data(channel_id)
                    break

        except Exception as e:
            self.reset_data(channel_id)
            await interaction.channel.send('Đã xảy ra lỗi trong trò chơi.')

async def setup(bot):
    await bot.add_cog(GuessNumCog(bot))