import discord
from discord.ext import commands
from discord import app_commands
from main import file_read_with_line

class roi(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @app_commands.command(name='100_rules_of_internet',description='100 rules of internet')
    @app_commands.describe(rule_number='Số thứ tự của các luật')
    async def roi(self, interaction: discord.Interaction, rule_number: str):
        rules = file_read_with_line('/d:/Coding/Bot-Chuot/txt_files/100_rules_of_internet.txt')
        found_rule = None

        # Convert special rule numbers for comparison
        special_numbers = {
            "3.141592653589793238462643383279502884197169399573105": "pi",
            "6.241592653589793238462643383279502888394338799146210": "plank"
        }

        # Search for the rule
        for rule in rules:
            rule_text = rule.strip()
            if rule_text.startswith(f"{rule_number}."):
                found_rule = rule_text
                break
            # Check for special number rules
            for special_num, symbol in special_numbers.items():
                if rule_text.startswith(special_num):
                    if rule_number in [symbol, special_num[:5]]:  # Match either symbol or first few digits
                        found_rule = f"{symbol}: {rule_text}"
                        break

        if found_rule:
            await interaction.response.send_message(found_rule)
        else:
            await interaction.response.send_message(f"Không tìm thấy luật số {rule_number}")

async def setup(bot):
    await bot.add_cog(roi(bot))