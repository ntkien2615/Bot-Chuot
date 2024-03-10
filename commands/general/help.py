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
            discord.SelectOption(label="Cảm ơn",value="4", emoji='💖',
                                 description="Cảm ơn những người hỗ trợ dev"),
        ]
        super().__init__(placeholder="Chọn một lựa chọn đi",
                         max_values=1, min_values=1, options=options)

    async def callback(self,interaction: discord.Interaction):
        if self.values[0] == "1":
            select_embed = discord.Embed(title='BOT INFO',
                                         description='Bot được phát triển bởi 1 người với mục đích mua vui là chính và phát triển kĩ năng.',
                                         color=discord.Color.random())
            select_embed.set_image(url='https://images.alphacoders.com/135/1353722.jpeg')
            await interaction.response.edit_message(embed=select_embed)


class DropdownMenu(discord.ui.View):  # Consistent naming
    def __init__(self):
        super().__init__()  # Timeout not needed
        self.add_item(SelectDropdown())


class HelpCog(commands.Cog):  # Correct PascalCase
    def __init__(self, bot):
        self.bot = bot

    def file_read(file_path, line_number):
        try:
            with open(file_path, "r") as f:
                lines = f.readlines()
            return lines[line_number - 1].strip()
        except IndexError:
            raise IndexError(f"Line number {line_number} is out of bounds for file {file_path}")

    @app_commands.command(name='help', description='trợ giúp')
    async def menu(self, interaction: discord.Interaction):
        view = DropdownMenu()
        description= file_read("./txt_files/help/help0.txt",1)
        embed_msg = discord.Embed(title="HELP COMMAND",
                                  description=description,
                                  color=discord.Color.random())
        embed_msg.set_thumbnail(
            url='https://images-ext-1.discordapp.net/external/4l1sSRH8ZyOAWjLY9KyMefCCwzKQqbQdZp5-FHo3pKg/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/104272908108.png?format=webp&quality=lossless&width=676&height=676')
        muc1 = file_read("./txt_files/help/help0.txt",2)
        embed_msg.add_field(name="BOT ĐÃ CHUYỂN NHÀ", value=muc1, inline=False)
        muc3 = file_read("./txt_files/help/help0.txt",3)
        embed_msg.add_field(name="Thay đổi và những khắc phục",
                            value=muc3, inline=False)
        muc2 =file_read("./txt_files/help/help0.txt",4)
        embed_msg.add_field(name="Tu bi con tìn niu...",
                            value=muc2, inline=False)
        muc4 = file_read("./txt_files/help/help0.txt",5)
        embed_msg.add_field(name="Bắt đầu", value= muc4, inline=False)
        hinhnen = file_read("./txt_files/help/help0.txt",6)
        embed_msg.add_field(name="Hình nền", value=hinhnen, inline=False)
        embed_msg.set_image(
            url='https://images7.alphacoders.com/134/1347439.jpeg')
        embed_msg.set_footer(text=f"Requested by {interaction.user}",
                             icon_url=interaction.user.avatar)

        await interaction.response.send_message(
            embed=embed_msg, view=view)  # Pass the view object


async def setup(bot):
    await bot.add_cog(HelpCog(bot))  # Use updated class name
