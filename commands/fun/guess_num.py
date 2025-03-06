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
    
    def reset_data(self):
        self.predictions.clear()
    
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
        self.reset_data()  # Fixed typo here
        self.number = self.random_number()
        await interaction.response.send_message('Đoán số từ 1 đến 100')

        try:
            def check(m):
                return m.author == interaction.user and m.channel == interaction.channel

            while True:
                message = await self.bot.wait_for('message', check=check, timeout=20.0)
                guess = int(message.content)
                result = self.check_win(guess)
                if result == 'win':
                    await interaction.followup.send(f'Chúc mừng {message.author.mention}, bạn đã đoán đúng số {self.number}!')
                    break
                elif result == 'low':
                    await interaction.followup.send(f'{message.author.mention}, số bạn đoán nhỏ hơn số cần đoán')
                else:
                    await interaction.followup.send(f'{message.author.mention}, số bạn đoán lớn hơn số cần đoán')
        except asyncio.TimeoutError:
            await message.channel.send(f'Hết giờ! Số cần đoán là {self.number}')
            self.reset_data()

async def setup(bot):
    await bot.add_cog(GuessNumCog(bot))