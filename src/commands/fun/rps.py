import discord
from discord.ext import commands
from discord import app_commands
import random


from src.commands.base_command import FunCommand


class rpsslash(FunCommand):

    def __init__(self, discord_bot):
        super().__init__(discord_bot)
        self.bot = discord_bot.bot

    @app_commands.command(
        name='rps',
        description='rock,paper,scissors aka kéo, búa, bao'
    )
    @app_commands.describe(value='chọn 1 trong 3')
    @app_commands.choices(value=[
        discord.app_commands.Choice(name="Kéo", value="Kéo"),
        discord.app_commands.Choice(name="Búa", value="Búa"),
        discord.app_commands.Choice(name="Bao", value="Bao")
    ])
    async def rps(self, interaction: discord.Interaction, value: str):
        npc = ['Kéo', 'Búa', 'Bao']
        npc_ran = random.choice(npc)
        npc_enemy = [
            'NPC', 'CHAT GPTEO', 'KHÁ BẢNH', 'bé Triết phi phai', 'tranbinh',
            'ambatukam'
        ]
        npc_enemy_ran = random.choice(npc_enemy)
        embed_msg = discord.Embed(title="RPS CLASSIC",
                                  color=discord.Color.random())
        embed_msg.add_field(name="",
                            value=f"{interaction.user} chọn: {value}",
                            inline=False)
        embed_msg.add_field(name="",
                            value=f"{npc_enemy_ran} chọn: {npc_ran}",
                            inline=False)
        if value == npc_ran:
            embed_msg.add_field(name="", value="Cả hai hòa", inline=False)
        elif (value == 'Kéo' and npc_ran == 'Búa') or (
            value == 'Búa' and npc_ran == 'Bao') or (value == 'Bao'
                                                     and npc_ran == 'Kéo'):
            embed_msg.add_field(
                name="",
                value=f"Bạn thua, trông bạn như vậy lại thua {npc_enemy_ran}",
                inline=False)
        else:
            embed_msg.add_field(name="", value="Bạn thắng!", inline=False)
        await interaction.response.send_message(embed=embed_msg)
