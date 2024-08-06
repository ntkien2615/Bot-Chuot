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
    async def gun(self, interaction:discord.Interaction, user: discord.Member = None):
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
            message_prefix = "đã chọn kết liễu bản thân và:"
            await interaction.response.send_message(f'<@{user.id}> {message_prefix}')
            await asyncio.sleep(2)
            if luck < 30:                
                await interaction.edit_original_response(content=f'<@{user.id}> {message_prefix}: BÙM!!!!!! {user} đã bị {random.choice(gun_kill)} trong {round(self.bot.latency*1000)} ms. Luck: {luck} < 30')
            else:
                await interaction.edit_original_response(content=f'<@{user.id}> {message_prefix}: TẠCH! {user} đã sống sót, thật may mắn vì {user} đã có giáp mũ tier 9. Luck: {luck} >= 30')
        else:
            message_prefix_2 = "đã bị chĩa súng vào mặt bởi"
            await interaction.response.send_message(f'<@{user.id}> {message_prefix_2} {interaction.user} và: ')
            await asyncio.sleep(2)
            if luck < 30:                
                await interaction.edit_original_response(content=f'<@{user.id}> {message_prefix_2} {interaction.user} và: BÙM!!!!!! {user} đã bị {random.choice(gun_kill)} trong {round(self.bot.latency*1000)} ms. Luck: {luck} < 30')
            else:
                await interaction.edit_original_response(content=f'<@{user.id}> {message_prefix_2} {interaction.user} và: TẠCH! {user} đã sống sót, thật may mắn vì {user} đã có giáp mũ tier 9. Luck: {luck} >= 30')

async def setup(bot):
    await bot.add_cog(gun(bot))