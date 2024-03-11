import discord
from discord.ext import commands
from discord import app_commands


class SelectDropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Info", value="1", emoji='🐭',
                                 description="Thông tin chung về bot"),
            discord.SelectOption(label="Lệnh nonslash",value="2", emoji="🐁",
                                 description="Các lệnh non-slash"),
            discord.SelectOption(label="Lệnh slash",value="3", emoji='🐀',
                                 description="Các lệnh slash"),
            discord.SelectOption(label="Về những người làm nên hôm nay",value="4", emoji='💖',
                                 description="Cảm ơn những người hỗ trợ dev"),
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
            select_embed_1 = discord.Embed(title='BOT INFO',
                                         description=self.file_read("./txt_files/help/help1.txt",1),
                                         color=discord.Color.random())
            select_embed_1.add_field(name='Sơ yếu lí lịch về bot',value='',inline=False)
            select_embed_1.add_field(name='',value=self.file_read("./txt_files/help/help1.txt",2),inline=False)
            select_embed_1.add_field(name='Thông tin về chủ bot',value='', inline=False)
            select_embed_1.add_field(name='',value=self.file_read("./txt_files/help/help1.txt",3),inline=False)
            select_embed_1.add_field(name='',value=self.file_read("./txt_files/help/help1.txt",4),inline=False)
            select_embed_1.add_field(name='',value=self.file_read("./txt_files/help/help1.txt",5),inline=False)
            select_embed_1.add_field(name='Lịch sử của Chuột',value=self.file_read("./txt_files/help/help1.txt",6),inline=False)
            select_embed_1.add_field(name='Chúng ta của tương lai',value=self.file_read("./txt_files/help/help1.txt",7),inline=False)
            select_embed_1.add_field(name='Thông tin về Coder (chắc chưa phải gọi là Dev đâu)',value=self.file_read("./txt_files/help/help1.txt",8),inline=False)
            select_embed_1.set_image(url='https://images.alphacoders.com/135/1353722.jpeg')
            await interaction.response.edit_message(embed=select_embed_1)
        elif self.values[0] == "2":
            select_embed_2 = discord.Embed(title="Các lệnh nonslash",
            description=self.file_read("./txt_files/help/help2.txt",1),
            color= discord.Color.random())
            select_embed_2.add_field(name= 'Prefix',value='Bot dùng dấu cộng (+) để thực hiện', inline= False)
            select_embed_2.add_field(name='Các lệnh',value='', inline=False)
            select_embed_2.add_field(name='', value=self.file_read('./txt_files/help/help2.txt',2),inline=False)
            select_embed_2.add_field(name='', value=self.file_read('./txt_files/help/help2.txt',3),inline=False)
            select_embed_2.add_field(name='', value=self.file_read('./txt_files/help/help2.txt',4),inline=False)
            select_embed_2.add_field(name='', value=self.file_read('./txt_files/help/help2.txt',5),inline=False)
            select_embed_2.add_field(name='', value=self.file_read('./txt_files/help/help2.txt',6),inline=False)
            select_embed_2.add_field(name='', value=self.file_read('./txt_files/help/help2.txt',7),inline=False)
            select_embed_2.set_image(url='https://i.pinimg.com/736x/33/db/52/33db52085d5eb336a6057b1f6750c12f.jpg')
            await interaction.response.edit_message(embed=select_embed_2)
        elif self.values[0] == "3":
            select_embed_3 = discord.Embed(title="Các lệnh Slash",
            description=self.file_read("./txt_files/help/help3.txt",1),
            color= discord.Color.random())
            select_embed_3.add_field(name='Các lệnh Chung: ',value=self.file_read('./txt_files/help/help3.txt',2), inline=True)
            select_embed_3.add_field(name='', value=self.file_read('./txt_files/help/help3.txt',3),inline=False)
            select_embed_3.add_field(name='', value=self.file_read('./txt_files/help/help3.txt',4),inline=False)
            select_embed_3.add_field(name='', value=self.file_read('./txt_files/help/help3.txt',5),inline=False)
            select_embed_3.add_field(name='Các lệnh giải trí: ', value=self.file_read('./txt_files/help/help3.txt',6),inline= True)
            select_embed_3.add_field(name='', value=self.file_read('./txt_files/help/help3.txt',7),inline=False)
            select_embed_3.add_field(name='', value=self.file_read('./txt_files/help/help3.txt',8),inline=False)
            select_embed_3.add_field(name='', value=self.file_read('./txt_files/help/help3.txt',9),inline=False)
            select_embed_3.add_field(name='Lệnh chưa phân loại', value='',inline=False)
            select_embed_3.add_field(name='', value=self.file_read('./txt_files/help/help3.txt',10),inline=False)
            select_embed_3.set_image(url='https://images3.alphacoders.com/125/1254519.jpg')
            await interaction.response.edit_message(embed=select_embed_3)        
        elif self.values[0] == "4":
            select_embed_4 = discord.Embed(title="Những người tạo ra bot",value=self.file_read('./txt_files/help/help4.txt',1), color=discord.Color.random())
            select_embed_4.add_field(name='k3v15l3v13tc05g(Cáo)', value=self.file_read('./txt_files/help/help4.txt',2),inline=False)
            select_embed_4.add_field(name='Chuột', value=self.file_read('./txt_files/help/help4.txt',3),inline=False)
            select_embed_4.add_field(name='Kyen', value=self.file_read('./txt_files/help/help4.txt',4),inline=False)
            select_embed_4.set_image(url='https://images-ext-2.discordapp.net/external/CgWKNYMqM2H_Q8rel9vzchKdh75oJzykfgId8tssbdQ/https/media.tenor.com/-q5sc5HU_SgAAAPo/the-goats-yes-king.mp4')
            await interaction.response.edit_message(embed=select_embed_4)
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
        description= self.file_read("./txt_files/help/help0.txt",1)
        embed_msg = discord.Embed(title="HELP COMMAND",
                                  description=description,
                                  color=discord.Color.random())
        embed_msg.set_thumbnail(
            url='https://images-ext-1.discordapp.net/external/4l1sSRH8ZyOAWjLY9KyMefCCwzKQqbQdZp5-FHo3pKg/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/104272908108.png?format=webp&quality=lossless&width=676&height=676')
        muc1 = self.file_read("./txt_files/help/help0.txt",2)
        embed_msg.add_field(name="BOT ĐÃ CHUYỂN NHÀ", value=muc1, inline=False)
        muc3 = self.file_read("./txt_files/help/help0.txt",3)
        embed_msg.add_field(name="Thay đổi và những khắc phục",
                            value=muc3, inline=False)
        muc2 = self.file_read("./txt_files/help/help0.txt",4)
        embed_msg.add_field(name="Tu bi con tìn niu...",
                            value=muc2, inline=False)
        muc4 = self.file_read("./txt_files/help/help0.txt",5)
        embed_msg.add_field(name="Hoàn thành", value= muc4, inline=False)
        hinhnen = self.file_read("./txt_files/help/help0.txt",6)
        embed_msg.add_field(name="Hình nền", value=hinhnen, inline=False)
        embed_msg.set_image(
            url='https://images7.alphacoders.com/134/1347439.jpeg')
        embed_msg.set_footer(text=f"Requested by {interaction.user}",
                             icon_url=interaction.user.avatar)

        await interaction.response.send_message(
            embed=embed_msg, view=view)  # Pass the view object


async def setup(bot):
    await bot.add_cog(HelpCog(bot))  # Use updated class name
