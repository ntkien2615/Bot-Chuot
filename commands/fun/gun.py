import discord
from discord.ext import commands
from discord import app_commands
import random
import asyncio


class gun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        
    @app_commands.command(name='gun_lỏ',description='Có cơ hội đưa bản thân lên bảng điểm số hoặc bắn ai đó cũng được (luck < 30 là chết nhé!)') 
    @app_commands.describe(user='Người bạn muốn bắn')
    async def gun(self, interaction:discord.Interaction, user: discord.Member):
        luck = random.randint(1,100)
        gun_kill = [
                    'NAGANT 1895 bắn',
                    'AK-47 bắn',
                    'M-60 kéo hết băng',
                    'Colt Python bắn',
                    'MOSSIN NAGANT tỉa',
                    'SAIGA-12 (S12K) shụt',
                    'USA12 kéo một lượt 20 viên đạn ghém'
                ]
    
        if (user == None) or (user == interaction.user):
            user = interaction.user
            await interaction.response.send_message(f'<@{user.id}> đã chọn kết liễu bản thân và: ')
            await asyncio.sleep(2)
            if luck < 30:                
                await interaction.edit_original_response(f'<@{user.id}> đã chọn kết liễu bản thân và: BÙM!!!!!! {user} đã bị {gun_kill} trong {round(self.bot.latency*1000)} ms. Luck của {user} là {luck} < 30')
            else:
                await interaction.edit_original_response(f'<@{user.id}> đã chọn kết liễu bản thân và: TẠCH! {user} đã sống sót, thật may mắn vì user đã có giáp mũ tier 9. Luck của {user} là {luck} >= 30')
        else:
            await interaction.response.send_message(f'<@{user.id}> đã bị chĩa súng vào mặt và: ')
            await asyncio.sleep(2)
            if luck < 30:                
                await interaction.edit_original_response(f'<@{user.id}> đã bị chĩa súng vào mặt và: BÙM!!!!!! {user} đã bị {gun_kill} trong {round(self.bot.latency*1000)} ms. Luck của {user} là {luck} < 30')
            else:
                await interaction.edit_original_response(f'<@{user.id}> đã bị chĩa súng vào mặt và: TẠCH! {user} đã sống sót, thật may mắn vì {user} đã có giáp mũ tier 9. Luck của {user} là {luck} >= 30')

async def setup(bot):
    await bot.add_cog(gun(bot))