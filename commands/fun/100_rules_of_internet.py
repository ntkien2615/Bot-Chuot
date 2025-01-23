import discord
from discord.ext import commands
from discord import app_commands
from database import RuleDatabase

class roi(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.rule_db = RuleDatabase()

    @app_commands.command(name='100_rules_of_internet', description='100 rules of internet')
    @app_commands.describe(rule_number='Số thứ tự của các luật')
    async def roi(self, interaction: discord.Interaction, rule_number: str):
        try:
            # Handle special cases for pi and plank
            if rule_number.lower() in ["pi", "plank"]:
                special_numbers = {
                    "pi": "3.141592653589793238462643383279502884197169399573105",
                    "plank": "6.241592653589793238462643383279502888394338799146210"
                }
                rule = self.rule_db.get_rule(special_numbers[rule_number.lower()])
                if rule:
                    await interaction.response.send_message(f"{rule_number}: {rule}")
                    return

            # Handle normal rules
            rule = self.rule_db.get_rule(rule_number)
            if rule:
                await interaction.response.send_message(f"{rule_number}. {rule}")
            else:
                await interaction.response.send_message(f"Không tìm thấy luật số {rule_number}")

        except ValueError:
            await interaction.response.send_message("Vui lòng nhập số hợp lệ")

async def setup(bot):
    await bot.add_cog(roi(bot))