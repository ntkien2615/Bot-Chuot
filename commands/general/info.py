import discord
from discord.ext import commands
from discord import app_commands


class SelectDropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Update", value="1",
                                 description="Thông tin cập nhật về bot"),
            discord.SelectOption(label="Về những người làm nên hôm nay",value="2",
                                 description="Cảm ơn những người hỗ trợ dev"),
            discord.SelectOption(label="Những thứ không ai hỏi", value="3", description="Những thứ ko ai hỏi tôi")
        ]
        super().__init__(placeholder="Chọn một lựa chọn đi",
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
            select_embed_1 = discord.Embed(title='Update',
                                         description=self.file_read("./txt_files/info/info0.txt",1),
                                         color=discord.Color.random())
            select_embed_1.add_field(name='Thêm các câu lệnh mới',value=self.file_read("./txt_files/info/info0.txt",2),inline=False)
            select_embed_1.add_field(name='Loại bỏ dần các lệnh non-slash',value=self.file_read("./txt_files/info/info0.txt",3),inline=False)
            select_embed_1.add_field(name='Thêm các dòng tin nhắn mới',value=self.file_read("./txt_files/info/info0.txt",4),inline=False)
            select_embed_1.set_image(url='https://images.alphacoders.com/135/1353722.jpeg')
            select_embed_1.set_footer(text=f"Requested by {interaction.user}",
                             icon_url=interaction.user.avatar)
            await interaction.response.edit_message(embed=select_embed_1)
        elif self.values[0] == "2":
            select_embed_2 = discord.Embed(title="Những người tạo ra bot",description=self.file_read('./txt_files/info/author.txt',1), color=discord.Color.random())
            select_embed_2.add_field(name='k3v15l3v13tc05g(Cáo)', value=self.file_read('./txt_files/info/author.txt',2),inline=False)
            select_embed_2.add_field(name='Chuột', value=self.file_read('./txt_files/info/author.txt',3),inline=False)
            select_embed_2.add_field(name='Kyen', value=self.file_read('./txt_files/info/author.txt',4),inline=False)
            select_embed_2.set_image(url='https://images-ext-2.discordapp.net/external/CgWKNYMqM2H_Q8rel9vzchKdh75oJzykfgId8tssbdQ/https/media.tenor.com/-q5sc5HU_SgAAAPo/the-goats-yes-king.mp4')
            select_embed_2.set_footer(text=f"Requested by {interaction.user}",
                             icon_url=interaction.user.avatar)
            await interaction.response.edit_message(embed=select_embed_2)
        elif self.values[0] == "3":
            select_embed_3 = discord.Embed(title="Những thứ không ai hỏi", description=self.file_read('./txt_files/info/no_one_ask.txt',1), color=discord.Color.random())
            await interaction.response.edit_message(embed=select_embed_3)

class DropdownMenu(discord.ui.View): 
    def __init__(self):
        super().__init__() 
        self.add_item(SelectDropdown())



class InfoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def file_read(self, file_path, line_number):
        try:
            with open(file_path, "r") as f:
                lines = f.readlines()
            return lines[line_number - 1].strip()
        except (IndexError, FileNotFoundError) as e:
            return None

    @app_commands.command(name='info', description='Về bot')
    async def menu(self, interaction: discord.Interaction):
        view = DropdownMenu()
        description= self.file_read("./txt_files/info/info0.txt",1)
        embed_msg = discord.Embed(title="INFO COMMAND",
                                  description=description,
                                  color=discord.Color.random())
        embed_msg.set_thumbnail(
            url='https://images-ext-1.discordapp.net/external/4l1sSRH8ZyOAWjLY9KyMefCCwzKQqbQdZp5-FHo3pKg/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/104272908108.png?format=webp&quality=lossless&width=676&height=676')
        await interaction.response.send_message(
            embed=embed_msg, view=view)


async def setup(bot):
    await bot.add_cog(InfoCog(bot))
