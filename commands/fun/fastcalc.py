import discord
from discord.ext import commands
from discord import app_commands
import random
import asyncio


from commands.base_command import FunCommand


class fastcalc(FunCommand):
    def __init__(self, bot):
        super().__init__(bot)

    def generate_simple_math_problem_and_result(self):
        operators = ['+', '-', '*', '/']
        operator = random.choice(operators)
        if operator == '/':
            a = random.randint(1, 100)
            b = random.randint(1, 100)
            while a % b != 0:
                a = random.randint(1, 100)
                b = random.randint(1, 100)
        else:
            a = random.randint(1, 100)
            b = random.randint(1, 100)
        result = eval(f'{a} {operator} {b}')
        return f'{a} {operator} {b} = ?', result

    def check_message_answer(self, message, result):
        try:
            return int(message.content) == result
        except ValueError:
            return False
    
    @app_commands.command(name='fast_calc', description='ai tính nhanh hơn')
    async def fastcalc(self, interaction: discord.Interaction):
        problem, result = self.generate_simple_math_problem_and_result()
        await interaction.response.send_message(f'Tính bài toán này trong 20s: **{problem}**')
        
        def check(m):
            return m.channel == interaction.channel
        
        try:
            while True:
                message = await self.bot.wait_for('message', check=check, timeout=20.0)
                if self.check_message_answer(message, result):
                    time_taken = (message.created_at - interaction.created_at).total_seconds()
                    await interaction.followup.send(f'{message.author.mention} trả lời đúng sau {time_taken:.1f} giây!')
                    break
                    
        except asyncio.TimeoutError:
            await interaction.followup.send(f'Hết giờ! Không ai trả lời đúng. Đáp án: {result}')
