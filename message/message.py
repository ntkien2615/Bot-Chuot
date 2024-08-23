from discord.ext import commands
import discord


class on_message(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def message(self, message):
        if message.author.bot:
            return
            await self.bot.process_commands(message)

        hi = ['chào', 'hi', 'hello', 'chao', 'xin chào', 'xin chao']
        if message.content.lower() in hi:
            await message.channel.send('chào cc')
            await self.bot.process_commands(message)

        bye = ['bye']
        if message.content.lower() in bye:
            await message.channel.send('sủi cmm luôn đi')
            await self.bot.process_commands(message)

        dead_chat = ['dead chat', 'dead chat xd','dead chat guys']
        if message.content.lower() in dead_chat:
            await message.channel.send('Dead mả cha m nhé')
            await self.bot.process_commands(message)

        russian = ['russian']
        if message.content.lower() in russian:
            await message.channel.send('NO RUSSIAN')
            await self.bot.process_commands(message)

        urk = ['ukrainian']
        if message.content.lower() in urk:
            await message.add_reaction("🤡")
            await self.bot.process_commands(message)

        sui = ['sui', 'sủi']
        for sui_word in sui:
            if sui_word in message.content.lower():
                await message.channel.send(
                    f'{message.author.display_name} *sẽ im lặng và biến mất...*')
                await self.bot.process_commands(message)

        dmcs = ['dmcs', 'đmcs']
        for dmcs_word in dmcs:
            if dmcs_word in message.content.lower():
                await message.reply(f'{message.author.display_name}')
                await message.channel.send(
                    "https://th.bing.com/th/id/R.2f1a48275690965a28da2930ea9d85dd?rik=%2fu7q7c6PPfn6wA&pid=ImgRaw&r=0"
                )
                await self.bot.process_commands(message)

        non = ['non']
        for non_word in non:
            if non_word in message.content.lower():
                await message.channel.send('Êu, có con gà non chưa kìa')
                await self.bot.process_commands(message)
        
        ngot = ['ngọt','ngot']
        for ngot_word in ngot:
            if ngot_word in message.content.lower():
                await message.reply('cẩn thận bị tiểu đường')
                await self.bot.process_commands(message)
        
        overthinking_words=['overthinking']
        for ovt_word in overthinking_words:
            if ovt_word in message.content.lower():
                await message.reply("Why we overthinking when we can ||Ov3Rdo$$3||. :3")
                await self.bot.process_commands(message)       

        about = ['về bot chuột', 'about "chuot" bot']
        for ab_word in about:
            if ab_word in message.content.lower():
                await message.reply('Về bot chuột. Bot chuột là con bot rất láo và ổn lào')
                await self.bot.process_commands(message)
                

async def setup(bot):
    await bot.add_cog(on_message(bot))
