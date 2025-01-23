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
        try:
            rule_index = int(rule_number) - 1  # Convert to 0-based index
            rules = file_read_with_line('/d:/Coding/Bot-Chuot/txt_files/100_rules_of_internet.txt', rule_index)
            
            if rules is None:
                await interaction.response.send_message(f"Không tìm thấy luật số {rule_number}")
                return

            # Special number handling
            special_numbers = {
                "3.141592653589793238462643383279502884197169399573105": "pi",
                "6.241592653589793238462643383279502888394338799146210": "plank"
            }

            # Check for special numbers
            if rule_number in ["pi", "plank"]:
                for special_num, symbol in special_numbers.items():
                    if rule_number == symbol and rules.startswith(special_num):
                        await interaction.response.send_message(f"{symbol}: {rules}")
                        return

            await interaction.response.send_message(rules)
            
        except ValueError:
            await interaction.response.send_message(f"Vui lòng nhập số hợp lệ")

async def setup(bot):
    await bot.add_cog(roi(bot))