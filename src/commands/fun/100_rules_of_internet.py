import discord
from discord.ext import commands
from discord import app_commands

# Simple rule database implementation
class RuleDatabase:
    def __init__(self):
        self.rules = {
            "1": "Do not talk about /b/",
            "2": "Do NOT talk about /b/",
            # Add more rules here
            "34": "If it exists, there is porn of it. No exceptions.",
            "35": "The exception to rule #34 is the citation of rule #34.",
            # Special rules
            "3.141592653589793238462643383279502884197169399573105": "Pi is exactly 3",
            "6.241592653589793238462643383279502888394338799146210": "Planck's constant is exactly 6"
        }
    
    def get_rule(self, rule_number):
        return self.rules.get(str(rule_number), None)

from src.commands.base_command import FunCommand


class roi(FunCommand):
    def __init__(self, discord_bot):
        super().__init__(discord_bot)
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