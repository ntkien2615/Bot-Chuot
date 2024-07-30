import discord
from discord.ext import commands
from discord import app_commands


class SelectDropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="General commands", value="1", 
                                 description="Các lệnh chung"),
            discord.SelectOption(label="Fun commands",value="2"
                                 description="Các lệnh giải trí"),
            discord.SelectOption(label="Unclassified commands",value="3",
                                 description="Lệnh này không biết phân loại ra sao")
        ]
        super().__init__(placeholder="Chọn một lựa chọn nào",
                         max_values=1, min_values=1, options=options)
    
    def file_read(self, file_path, line_number):
        try:
            with open(file_path, "r") as f:
                lines = f.readlines()
            return lines[line_number - 1].strip()
        except (IndexError, FileNotFoundError) as e:
            return None

    async def callback(self,interaction: discord.Interaction):
        if self.values[0] == "1":
            select_embed_1 = discord.Embed(title='Các lệnh chung',
                                         description="",
                                         color=discord.Color.random())
            select_embed_1.add_field(name='/avatar',value=self.file_read("./txt_files/help/general_commands.txt",2),inline=False)
            select_embed_1.add_field(name='/help',value=self.file_read("./txt_files/help/general_commands.txt",3),inline=False)
            select_embed_1.add_field(name='/info',value=self.file_read("./txt_files/help/general_commands.txt",4),inline=False)
            select_embed_1.add_field(name="/ping", value=self.file_read(".txt_files/help/general_commands.txt",5), inline=True)
            select_embed_1.set_footer(text=f"Requested by {interaction.user}",
                             icon_url=interaction.user.avatar)
            await interaction.response.edit_message(embed=select_embed_1)
        elif self.values[0] == "2":
            select_embed_2 = discord.Embed(title="Các lệnh giải trí",
            description='',
            color= discord.Color.random())
            select_embed_2.add_field(name='/codejoke', value=self.file_read('./txt_files/help/fun_commands.txt',2),inline=False)
            select_embed_2.add_field(name='/dice', value=self.file_read('./txt_files/help/fun_commands.txt',3),inline=False)
            select_embed_2.add_field(name='/fakemsg', value=self.file_read('./txt_files/help/fun_commands.txt',4),inline=False)
            select_embed_2.add_field(name='/im', value=self.file_read('./txt_files/help/fun_commands.txt',5),inline=False)
            select_embed_2.add_field(name='/mp5_leg', value=self.file_read('./txt_files/help/fun_commands.txt',6),inline=False)
            select_embed_2.add_field(name='/phenis', value=self.file_read('./txt_files/help/fun_commands.txt',7),inline=False)
            select_embed_2.set_footer(text=f"Requested by {interaction.user}",
                             icon_url=interaction.user.avatar)
            await interaction.response.edit_message(embed=select_embed_2)
        elif self.values[0] == "3":
            select_embed_3 = discord.Embed(title="Các lệnh chưa phân loại được",
            description='',
            color= discord.Color.random())
            select_embed_3.add_field(name='/search',value=self.file_read('./txt_files/help/help3.txt',2), inline=False)
            select_embed_3.add_field(name='/aiask', value=self.file_read('./txt_files/help/help3.txt',3),inline=False)
            select_embed_3.set_footer(text=f"Requested by {interaction.user}",
                             icon_url=interaction.user.avatar)
            await interaction.response.edit_message(embed=select_embed_3)        
class DropdownMenu(discord.ui.View): 
    def __init__(self):
        super().__init__() 
        self.add_item(SelectDropdown())



class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def file_read(self, file_path, line_number):
        try:
            with open(file_path, "r") as f:
                lines = f.readlines()
            return lines[line_number - 1].strip()
        except (IndexError, FileNotFoundError) as e:
            return None

    @app_commands.command(name='help', description='trợ giúp')
    async def menu(self, interaction: discord.Interaction):
        view = DropdownMenu()
        embed_msg = discord.Embed(title="HELP COMMAND",
                                  description="Dưới đây là các lệnh hiện tại của Chuột, sau này admin sẽ cập nhật thêm",
                                  color=discord.Color.random())
        embed_msg.set_thumbnail(
            url='https://images-ext-1.discordapp.net/external/4l1sSRH8ZyOAWjLY9KyMefCCwzKQqbQdZp5-FHo3pKg/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/104272908108.png?format=webp&quality=lossless&width=676&height=676')
        embed_msg.set_footer(text=f"Requested by {interaction.user}",
                             icon_url=interaction.user.avatar)

        await interaction.response.send_message(
            embed=embed_msg, view=view)


async def setup(bot):
    await bot.add_cog(HelpCog(bot))
