from discord.ext import commands
import random
import time

class MessageCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.processed_messages = set()
        self.message_timestamps = {}
        self.cleanup_interval = 3600  # 1 hour
        self.last_cleanup = time.time()
        self.consecutive_message_count = {}
        self.responses_dict = {
            'hi': 'chào cc',
            'bye': 'sủi cmm luôn đi',
            'dead_chat': ['dead cc', 'Dead mả cha m nhé'],
            'russian': 'NO RUSSIAN',
            'ukrainian': None,
            'sui': lambda m: f'{m.author.display_name} *sẽ im lặng và biến mất...*',
            'dmcs': lambda m: f'{m.author.display_name}\nhttps://th.bing.com/th/id/R.2f1a48275690965a28da2930ea9d85dd?rik=%2fu7q7c6PPfn6wA&pid=ImgRaw&r=0',
            'non': 'Êu, có con gà non chưa kìa',
            'ngot': 'cẩn thận bị tiểu đường',
            'overthinking': "Why we overthinking when we can ||Ov3Rdo$$3||. :3",
            'about': 'Về bot chuột. Bot chuột là con bot rất láo và ổn lào, và bạn gõ slash /info đấy dumb, tao không hiểu tại sao thằng kia nó lại làm cái này, bot có lệnh slash hết rồi',
            'kevin': '<@868475751459094580>',
            'pholotino': 'Không biết anh Thành Vũ có biết Tú có Ny hay không😗😗 ...',  # shortened for brevity
            'jack': [
                'Idol tôi là JACK đó rồi sao 🙂? Đối với những người ghét JACK,ĐÓM...',  # shortened for brevity
                'Đừnq 👐 bao zờ 😏 gkét 😡 a Jack 😢😭...'  # shortened for brevity
            ],
            'link': 'https://media.discordapp.net/attachments/883268139922636820/1287350064276045824/278755226_745698233463800_1291647474017004061_n.png?ex=66f139ad&is=66efe82d&hm=691315948a3b26a3d54e02820608b560bba49b35bf5b5c7b6812774e01660bd5&=&format=webp&quality=lossless&width=200&height=252',
            'thai_land': [
                'Ăn lẩu cay 5-3',
                "thai lan tuon loi",
                "đá ngu như bò bày đặt kêu thủ môn lên",
                "https://media.discordapp.net/attachments/882972000585388042/1325482803709743124/472357483_1876023823201095_175475186867281871_n.png?ex=677bf38e&is=677aa20e&hm=2cfb45bcb451705ddacbabb4dd447ca2cf0dc92885b9eb25e9d59bf41476ac95&=&format=webp&quality=lossless&width=400&height=225"
            ]
        }

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if message.author.bot or message.id in self.processed_messages:
                return

            self.processed_messages.add(message.id)
            current_time = time.time()

            if current_time - self.last_cleanup > self.cleanup_interval:
                self.cleanup_processed_messages()
                self.last_cleanup = current_time

            message_key = (message.channel.id, message.author.id, message.content)
            if message_key in self.message_timestamps and current_time - self.message_timestamps[message_key] < 2:
                return

            self.message_timestamps[message_key] = current_time

            # Track consecutive messages
            if message_key not in self.consecutive_message_count:
                self.consecutive_message_count[message_key] = 0
            self.consecutive_message_count[message_key] += 1

            if self.consecutive_message_count[message_key] > 4:
                return

            responses = {
                'hi': ['chào', 'hi', 'hello', 'chao'],
                'bye': ['bye'],
                'dead_chat': ['dead chat'],
                'russian': ['russian'],
                'ukrainian': ['ukrainian'],
                'sui': ['sui', 'sủi'],
                'dmcs': ['dmcs', 'đmcs'],
                'non': ['non'],
                'ngot': ['ngọt', 'ngot'],
                'overthinking': ['overthinking'],
                'about': ['về bot chuột', 'about "chuot" bot'],
                'kevin': ['kevin', 'kê vin'],
                'pholotino': ['florentino', 'fo lon ti no', 'pholotino'],
                'jack': ['jack', 'trịnh trần phương tuấn', 'j97', 'trinh tran phuong tuan', 'meo meo', '5 củ', 'jack bến tre'],
                'link': ['link'],
                "thai_land": ["thailand", "thái lan", "thai land", "thái land", "thái lan", "thailand đất nước của nụ cười", "thai land đất nước của nụ cười", "thái land đất nước của nụ cười"]
            }

            message_words = message.content.lower().split()
            for key, keywords in responses.items():
                if any(keyword in message_words if ' ' not in keyword else keyword in message.content.lower() for keyword in keywords):
                    response = self.get_response(key, message)
                    if response:
                        await message.channel.send(response)
                    break

            # Reset the counter if a different message is sent
            self.consecutive_message_count[message_key] = 0

        except Exception as e:
            print(f"Error processing message: {e}")

    def cleanup_processed_messages(self):
        current_time = time.time()
        self.processed_messages = {msg_id for msg_id in self.processed_messages if current_time - self.message_timestamps.get(msg_id, 0) < self.cleanup_interval}
        self.message_timestamps = {key: timestamp for key, timestamp in self.message_timestamps.items() if current_time - timestamp < self.cleanup_interval}
        self.consecutive_message_count = {key: count for key, count in self.consecutive_message_count.items() if current_time - self.message_timestamps.get(key, 0) < self.cleanup_interval}

    def get_response(self, key, message):
        response = self.responses_dict.get(key)
        if callable(response):
            return response(message)
        elif isinstance(response, list):
            return random.choice(response)
        return response

async def setup(bot):
    await bot.add_cog(MessageCog(bot))

