import discord
from discord.ext import commands
from discord import app_commands
import random
import asyncio

class taixiuslash(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.predictions = {}  # Store user predictions

    def three_dice_and_res(self):
        dice = [random.randint(1,6) for i in range(3)]
        res = sum(dice)

        return dice, res

    def check_win(self,res):
        if res < 11:
            return 'xỉu'
        else:
            return 'tài'

    def get_data(self):
        if not hasattr(self, 'predictions'):
            self.predictions = {}
        return self.predictions

    def reset_data(self):
        self.predictions.clear()

    def is_valid_prediction(self, content):
        content = content.lower()
        if content in ['tài', 'tai', 't']:
            return 'tài'
        elif content in ['xỉu', 'xiu', 'x']:
            return 'xỉu'
        return None

    @app_commands.command(name='tai_xiu', description='Chơi tài xỉu (không có tiền, chỉ vui thôi)')
    async def tai_xiu(self,interaction: discord.Interaction):
        self.reset_data()  # Clear previous predictions
        dice, res =  self.three_dice_and_res()
        win = self.check_win(res)
        embed_msg_1 = discord.Embed(title=f'Tài Xỉu R34',description='Trong vòng 20s, nhập Tài,tài,T,t cho tài hoặc X,x,xỉu,xỉu cho Xỉu. Chỉ nhận lần nhập cuối cùng, các lần nhập không liên quan sẽ bị bỏ qua',color=discord.Color.random())
        await interaction.response.send_message(embed=embed_msg_1)

        def check(m):
            return m.channel == interaction.channel
        
        try:
            while True:
                message = await self.bot.wait_for('message', check=check, timeout=20.0)
                prediction = self.is_valid_prediction(message.content)
                if prediction:
                    self.predictions[message.author.id] = prediction
                    await message.add_reaction('✔️')  # Add checkmark reaction for valid predictions
                    
        except asyncio.TimeoutError:
            winners = []
            for user_id, pred in self.predictions.items():
                if pred == win:
                    user = interaction.guild.get_member(user_id)
                    if user:
                        winners.append(user.display_name)
            
            winner_text = "Không ai thắng cả!" if not winners else f"Người thắng: {', '.join(winners)}"
            await interaction.followup.send(f'Kết quả 3 xúc sắc: {dice} = {res}, tức là {win}\n{winner_text}')
            self.reset_data()  # Clear predictions after game ends

async def setup(bot):
    await bot.add_cog(taixiuslash(bot))