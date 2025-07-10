import discord
from discord.ext import commands
from discord import app_commands
from commands.base_command import GeneralCommand
import random
import os


class RulesCommand(GeneralCommand):
    """Command to get rules from the 100 rules of internet."""
    
    def __init__(self, bot):
        super().__init__(bot)
        self.name = "rules"
        self.description = "Xem các quy tắc của Internet"
        self.rules_file_path = "txt_files/100_rules_of_internet.txt"

    def load_rules(self):
        """Load rules from the text file."""
        try:
            if not os.path.exists(self.rules_file_path):
                return None
            
            with open(self.rules_file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                rules = []
                for line in content.split('\n'):
                    line = line.strip()
                    if line and not line.startswith('//'):
                        rules.append(line)
                return rules
        except Exception as e:
            print(f"Error loading rules: {e}")
            return None

    @app_commands.command(name='rules', description='Xem quy tắc ngẫu nhiên của Internet hoặc quy tắc cụ thể')
    async def rules(self, interaction: discord.Interaction, rule_number: int = None):
        try:
            rules = self.load_rules()
            if not rules:
                await interaction.response.send_message("Không thể tải quy tắc Internet", ephemeral=True)
                return

            if rule_number is None:
                # Random rule
                rule = random.choice(rules)
                embed = discord.Embed(
                    title="🌐 Quy tắc ngẫu nhiên của Internet",
                    description=rule,
                    color=discord.Color.random()
                )
            else:
                # Specific rule
                matching_rules = [r for r in rules if r.startswith(f"{rule_number}.")]
                if not matching_rules:
                    await interaction.response.send_message(f"Không tìm thấy quy tắc số {rule_number}", ephemeral=True)
                    return
                
                rule = matching_rules[0]
                embed = discord.Embed(
                    title=f"🌐 Quy tắc số {rule_number} của Internet",
                    description=rule,
                    color=discord.Color.blue()
                )

            embed.set_footer(text=f"Yêu cầu bởi {interaction.user.display_name}", 
                           icon_url=interaction.user.display_avatar.url)
            await interaction.response.send_message(embed=embed)

        except Exception as e:
            await interaction.response.send_message("Có lỗi xảy ra khi lấy quy tắc", ephemeral=True)
            print(f"Rules command error: {e}")


async def setup(bot):
    await bot.add_cog(RulesCommand(bot))
