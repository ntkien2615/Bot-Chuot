import discord
from discord.ext import commands
from discord import app_commands
import random
import asyncio

from src.commands.base_command import FunCommand


class TaiXiuView(discord.ui.View):
    def __init__(self, game_instance):
        super().__init__(timeout=20.0)
        self.game = game_instance
        
    @discord.ui.button(label='🎯 TÀI', style=discord.ButtonStyle.green, emoji='🔥')
    async def tai_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.game.predictions[interaction.user.id] = 'tài'
        await interaction.response.send_message(f"🎯 {interaction.user.display_name} đã chọn **TÀI**!", ephemeral=True)
        
    @discord.ui.button(label='🎯 XỈU', style=discord.ButtonStyle.red, emoji='❄️')
    async def xiu_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.game.predictions[interaction.user.id] = 'xỉu'
        await interaction.response.send_message(f"🎯 {interaction.user.display_name} đã chọn **XỈU**!", ephemeral=True)
        
    async def on_timeout(self):
        # Disable all buttons when timeout
        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True


class taixiuslash(FunCommand):
    def __init__(self, discord_bot):
        super().__init__(discord_bot)
        self.bot = discord_bot.bot
        self.predictions = {}  # Store user predictions

    def three_dice_and_res(self):
        dice = [random.randint(1,6) for i in range(3)]
        res = sum(dice)
        return dice, res

    def dice_to_emoji(self, dice_value):
        """Convert dice number to emoji"""
        dice_emojis = {
            1: "⚀", 2: "⚁", 3: "⚂", 
            4: "⚃", 5: "⚄", 6: "⚅"
        }
        return dice_emojis.get(dice_value, "🎲")

    def format_dice_result(self, dice):
        """Format dice results with emojis"""
        dice_emojis = [self.dice_to_emoji(d) for d in dice]
        return " ".join(dice_emojis)

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
    async def tai_xiu(self, interaction: discord.Interaction):
        self.reset_data()  # Clear previous predictions
        
        # Create initial embed
        embed = discord.Embed(
            title="🎲 TÀI XỈU 🎲",
            description="🎯 **Chọn TÀI hoặc XỈU trong vòng 20 giây!**\n\n"
                       "🔥 **TÀI**: Tổng xúc sắc ≥ 11\n"
                       "❄️ **XỈU**: Tổng xúc sắc < 11\n\n"
                       "📝 Nhấn nút bên dưới để chọn!",
            color=discord.Color.gold()
        )
        embed.set_footer(text="⏰ Thời gian còn lại: 20 giây")
        
        # Create view with buttons
        view = TaiXiuView(self)
        await interaction.response.send_message(embed=embed, view=view)
        
        # Wait for timeout
        await asyncio.sleep(20)
        
        # Generate results
        dice, res = self.three_dice_and_res()
        win = self.check_win(res)
        dice_display = self.format_dice_result(dice)
        
        # Determine winners
        winners = []
        for user_id, pred in self.predictions.items():
            if pred == win:
                if interaction.guild:
                    user = interaction.guild.get_member(user_id)
                    if user:
                        winners.append(user.display_name)
        
        # Create result embed
        result_color = discord.Color.green() if win == 'tài' else discord.Color.red()
        win_emoji = "🔥" if win == 'tài' else "❄️"
        
        result_embed = discord.Embed(
            title=f"🎲 KẾT QUẢ TÀI XỈU {win_emoji}",
            color=result_color
        )
        
        result_embed.add_field(
            name="🎲 Xúc sắc",
            value=f"{dice_display}\n({dice[0]} + {dice[1]} + {dice[2]} = {res})",
            inline=False
        )
        
        result_embed.add_field(
            name=f"{win_emoji} Kết quả",
            value=f"**{win.upper()}**",
            inline=True
        )
        
        if winners:
            winner_text = "🏆 " + ", ".join(winners)
            result_embed.add_field(
                name="🎉 Người thắng",
                value=winner_text,
                inline=True
            )
        else:
            result_embed.add_field(
                name="😢 Kết quả",
                value="Không ai thắng cả!",
                inline=True
            )
            
        # Add some fun stats
        total_players = len(self.predictions)
        if total_players > 0:
            result_embed.add_field(
                name="📊 Thống kê",
                value=f"Tổng người chơi: {total_players}",
                inline=False
            )
        
        # Disable buttons and send result
        await view.on_timeout()
        await interaction.edit_original_response(view=view)
        await interaction.followup.send(embed=result_embed)
        
        self.reset_data()  # Clear predictions after game ends