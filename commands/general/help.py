import discord
from discord.ext import commands
from discord import app_commands


class SelectDropdown(discord.ui.Select):  # Clearer class name
    def __init__(self):
        options = [
            discord.SelectOption(label="Info", emoji='🐭',
                                 description="Thông tin chung về bot"),
            discord.SelectOption(label="Lệnh nonslash",
                                 emoji="🐁", description="Các lệnh non-slash",),
            discord.SelectOption(label="Lệnh slash", emoji='🐀',
                                 description="Các lệnh slash",),
            discord.SelectOption(label="Cảm ơn", emoji='💖',
                                 description="Cảm ơn những người hỗ trợ dev",)
        ]
        super().__init__(placeholder="Chọn một lựa chọn đi",
                         max_values=1, min_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        selected_option = self.values[0]
        response = f"You selected: {selected_option}"  # Dynamic response
        # Edit original message
        await interaction.response.edit_message(content=response)


class DropdownMenu(discord.ui.View):  # Consistent naming
    def __init__(self):
        super().__init__()  # Timeout not needed
        self.add_item(SelectDropdown())


class HelpCog(commands.Cog):  # Correct PascalCase
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='help', description='trợ giúp')
    async def menu(self, interaction: discord.Interaction):
        view = DropdownMenu()

        embed_msg = discord.Embed(title="HELP COMMAND",
                                  description="Đây là help command, nếu bạn đọc được cái này, bạn đã giải tỏa căng thẳng cho thằng dev xàm lờ",
                                  color=discord.Color.random())
        embed_msg.set_thumbnail(
            url='https://images-ext-1.discordapp.net/external/4l1sSRH8ZyOAWjLY9KyMefCCwzKQqbQdZp5-FHo3pKg/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/104272908108.png?format=webp&quality=lossless&width=676&height=676')
        muc1 = 'Hiện tại bot đã chuyển từ replit sang codesandbox (do replit không cho phép sử dụng bên thứ 3 để duy trì code) nên hiện tại bot sẽ rất lộn xộn nên thông cảm giùm'
        embed_msg.add_field(name="BOT ĐÃ CHUYỂN NHÀ", value=muc1, inline=False)
        muc3 = 'Bot đã đang và sẽ có sự thay đổi trong các lệnh và khắc phục những lỗi do code đã được sử dụng trong replit, trong tương lai anh coder này sẽ tối ưu bot nhiều hơn giúp hiệu quả bot được nâng cao'
        embed_msg.add_field(name="Thay đổi và những khắc phục",
                            value=muc3, inline=False)
        muc2 = 'Bot sẽ liên tục cập nhật những tính năng nên cứ đợi đi, bên này mượt hơn và ít ping hơn nên dễ làm việc, và cảm ơn vì đã đợi :3'
        embed_msg.add_field(name="Tu bi con tìn niu...",
                            value=muc2, inline=False)
        hinhnen = 'Cái hình để chưng bên dưới sẽ ghi nguồn sau'
        embed_msg.add_field(name="Hình nền", value=hinhnen, inline=False)
        embed_msg.set_image(
            url='https://images7.alphacoders.com/134/1347439.jpeg')
        embed_msg.set_footer(text=f"Requested by {interaction.user}",
                             icon_url=interaction.user.avatar)

        await interaction.response.send_message(
            embed=embed_msg, view=view)  # Pass the view object


async def setup(bot):
    await bot.add_cog(HelpCog(bot))  # Use updated class name
