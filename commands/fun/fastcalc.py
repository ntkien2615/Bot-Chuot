import discord
from discord.ext import commands
from discord import app_commands
import random
import asyncio


class fastcalc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
        await interaction.response.send_message(f'Tính bài toán này trong 20s: **{problem}**:')
        try:
            message = await self.bot.wait_for('message', check=lambda m: m.author == interaction.user, timeout=20)
        except asyncio.TimeoutError:
            await interaction.followup.send('Hết giờ! Thì ra nhiều người cũng lạm dụng máy tính cầm tay quá. Đáp án: {result}')
        else:
            if self.check_message_answer(message, result):
                time_taken = (message.created_at - interaction.created_at).total_seconds()
                await interaction.followup.send(f'{interaction.user.mention} trả lời nhanh nhất sau {time_taken:.1f} giây!')
async def setup(bot):
    await bot.add_cog(fastcalc(bot))
