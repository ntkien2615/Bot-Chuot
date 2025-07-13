import discord
from discord.ext import commands
from discord import app_commands
import os

# Simple rule database implementation
class RuleDatabase:
    def __init__(self, file_path):
        self.rules = {}
        self.load_rules(file_path)

    def load_rules(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('. ', 1)
                if len(parts) == 2:
                    self.rules[parts[0]] = parts[1]

    def get_rule(self, rule_number):
        return self.rules.get(str(rule_number), None)

from src.commands.base_command import FunCommand


class roi(FunCommand):
    def __init__(self, discord_bot):
        super().__init__(discord_bot)
        # Correctly locate the rules file
        rules_file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'txt_files', '100_rules_of_internet.txt')
        self.rule_db = RuleDatabase(rules_file_path)

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