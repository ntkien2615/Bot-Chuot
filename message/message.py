from discord.ext import commands
import discord


class on_message(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def message(self, message):
        hi = ['chào', 'hi', 'hello', 'chao', 'xin chào', 'xin chao']
        if message.content.lower() in hi:
            await message.channel.send('chào cc')
            await self.bot.process_commands(message)

        bye = ['bye']
        if message.content.lower() in bye:
            await message.channel.send('sủi cmm luôn đi')
            await self.bot.process_commands(message)

        dead_chat = ['dead chat', 'dead chat xd']
        if message.content.lower() in dead_chat:
            await message.channel.send('Dead cc')
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
                await message.channel.send('Êu, có con gà green chưa kìa')
                await self.bot.process_commands(message)
        
        ngot = ['ngọt','ngot']
        for ngot_word in ngot:
            if ngot_word in message.content.lower():
                await message.reply('cẩn thận bị tiểu đường')
                await self.bot.process_commands(message)
        
        overthinking_words = set(['overthinking'])
        already_replied = set()
        for ovt_word in overthinking_words:
            if (ovt_word in message.content.lower()) and (ovt_word not in already_replied):
                await message.reply("Why we overthinking because we can ||overdose||. :3")
                already_replied.add(ovt_word)
                await self.bot.process_commands(message)
                break

async def setup(bot):
    await bot.add_cog(on_message(bot))
