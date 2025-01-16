from discord.ext import commands
import random
import discord
import time

class MessageCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.processed_messages = set()
        self.message_timestamps = {}
        self.cleanup_interval = 3600  # 1 hour
        self.last_cleanup = time.time()
        self.consecutive_message_count = {}

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
            if message_key in self.message_timestamps and current_time - self.message_timestamps[message_key] < 5:
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

            for key, keywords in responses.items():
                if any(keyword in message.content.lower() for keyword in keywords):
                    response = self.get_response(key, message)
                    if response:
                        bot_message = await message.channel.send(response)
                        await bot_message.delete(delay=10)
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
        responses = {
            'hi': 'chào cc',
            'bye': 'sủi cmm luôn đi',
            'dead_chat': random.choice(['dead cc', 'Dead mả cha m nhé']),
            'russian': 'NO RUSSIAN',
            'ukrainian': None,
            'sui': f'{message.author.display_name} *sẽ im lặng và biến mất...*',
            'dmcs': f'{message.author.display_name}\nhttps://th.bing.com/th/id/R.2f1a48275690965a28da2930ea9d85dd?rik=%2fu7q7c6PPfn6wA&pid=ImgRaw&r=0',
            'non': 'Êu, có con gà non chưa kìa',
            'ngot': 'cẩn thận bị tiểu đường',
            'overthinking': "Why we overthinking when we can ||Ov3Rdo$$3||. :3",
            'about': 'Về bot chuột. Bot chuột là con bot rất láo và ổn lào, và bạn gõ slash /info đấy dumb, tao không hiểu tại sao thằng kia nó lại làm cái này, bot có lệnh slash hết rồi',
            'kevin': '<@868475751459094580>',
            'pholotino': 'Không biết anh Thành Vũ có biết Tú có Ny hay không😗😗 chúng tôi biết rằng tú có ny là người chơi khá nổi tiếng với con bài Florentino😲😲 ngày hôm nay anh ta đi cầm Florentino và chơi rất hay😎 trận thi đấu vừa xong là trận thi đấu mà chúng ta có thể thấy rằng là các bạn khán giả cũng có kĩ năng rất tốt- đặc biệt là người chơi bên phía của đội tuyển Đồng 5 đội tuyển Trái Đất đó là Tú có Ny🥳 tôi thấy rằng anh ta chưa để cái tốc biến mình hồi được hiện xanh quá lâu anh ta sử dụng ngay lập tức bằng những tình huống mở giao tranh của mình và chính Tú có Ny là MVP của trận thi đấu này với 14.0 điểm MVP😎😎. Một tình huống mà có lẽ Flo đang làm quá nhiều điều🤕🤕 những tình huống bông muq muq muq muq, bỏ chạy với Flo, Flo đang múa quá nhức nách, phải nói là Flo võ công quá cao cường🔪🔪😏😏. Và đây là Florentino, Florentino ui 🥶🥶👿👿😳một cái tình huống phải nói là cực gắt.👿Tú có Ny và người chơi này có lẽ sẽ có Ny thôi🥴🥴đánh quá ghê. Những tình huống bông hoa bông hủng phải nói là đúng top 1, buff bẩn🥵🥵. Quá ghê gớm....🌚😳 Và đây là Folontilô!😱😱 Folontilô ui... 🥶🥶👿😳một tình huống múa phải nói là cực 👿gắt!! *music🤯 Thẹn thùng nhìn em quay gót đi mãi😞😞💔 Anh đứng chết lặng trong mưa😭😭 Dù rằng bên😊😊 em đã có ai Nhưng nơi đây anh 🤗🤗🥱vẫn còn chờ...',
            'jack': random.choice([
                'Idol tôi là JACK đó rồi sao 🙂? Đối với những người ghét JACK,ĐÓM chúng tôi là Ruồi đó rồi sao 🙂? Liên quan gì ? Tôi nói idol tôi đẹp chứ đâu phải mấy người nói đâu ? Ủa bị gì vậy? Những người fan JACK cũng đều bị anti mấy người chửi đó ? Không liên quan lắm nhưng mà chuyện cuat người ta xía mồm vào làm gì ? Rảnh quá đi soi chuyện người khác có thấy trẻ con quá không?Lúc JACK chưa lên tiếng gì cả thì cũng bu vào xỉ xó giờ JACK lên tiếng rồi thì cũng xỉ xó bu vào phẫn nộ bài viết.rồi làm vậy có ích gì? Có tốt lành gì không? Rồi những người nổi tiếng khác cũng là fan ẢNH vào cmt tus ẢNH cũng bay vô chửi họ ? Ủa rồi người mình ngưỡng mộ fan người mình anti rồi tức bay vào chửi à ? Nói này nói nọ bảo “Thiếu fame” ủa thiếu fane là thiếu fame làm sao? Ủa tự nhiên fan anh JACK cái bảo thiếu fame rảnh vừa thôi chứ? Vào group của ĐÓM rồi vào từng bài viết chửi ? Ủa làm vậy để cho người khác ghét mình hơn à? Mấy người là anti thì có liên quan gì tới người mà mình anti không mà bu vào chửi ? nói chung là We’re no strangers to love, You know the rules and so do I. A full commitment’s what I’m thinking of You wouldnt get this from any other guy. I just wanna tell you how I’m feeling, Gotta make you understand... Never gonna give you up, Never gonna let you down, Never gonna run around and desert you.',
                'Đừnq 👐 bao zờ 😏 gkét 😡 a Jack 😢😭, đom đóm 👉 củg zậy 😉đừg 🤫 bao zờ 😠 gkét 🤬 a ♥️😍😍 đom đóm xẽ 🙂 trịu hớt 🤯 trịu hớt😣😵 ta^t kả😇 la j fan😔 đừg lam 😠 a Jack🤩 tổn tkưg 😭😭 đom đóm xẽ đau 🙁 nkư dao kắt 🔪🔪 kim đăm 💔💔Đừnq 👐 bao zờ 😏 gkét 😡 a Jack 😢😭, đom đóm 👉 củg zậy 😉đừg 🤫 bao zờ 😠 gkét 🤬 a ♥️😍😍 đom đóm xẽ 🙂 trịu hớt 🤯 trịu hớt😣😵 ta^t kả😇 la j fan😔 đừg lam 😠 a Jack🤩 tổn tkưg 😭😭 đom đóm xẽ đau 🙁 nkư dao kắt 🔪🔪 kim đăm 💔💔Đừnq 👐 bao zờ 😏 gkét 😡 a Jack 😢😭, đom đóm 👉 củg zậy 😉đừg 🤫 bao zờ 😠 gkét 🤬 a ♥️😍😍 đom đóm xẽ 🙂 trịu hớt 🤯 trịu hớt😣😵 ta^t kả😇 la j fan😔 đừg lam 😠 a Jack🤩 tổn tkưg 😭😭 đom đóm xẽ đau 🙁 nkư dao kắt 🔪🔪 kim đăm 💔💔'
            ]),
            'link': 'https://media.discordapp.net/attachments/883268139922636820/1287350064276045824/278755226_745698233463800_1291647474017004061_n.png?ex=66f139ad&is=66efe82d&hm=691315948a3b26a3d54e02820608b560bba49b35bf5b5c7b6812774e01660bd5&=&format=webp&quality=lossless&width=200&height=252',
            'thai_land': random.choice([
                'Ăn lẩu cay 5-3',
                "thai lan tuon loi",
                "đá ngu như bò bày đặt kêu thủ môn lên",
                "https://media.discordapp.net/attachments/882972000585388042/1325482803709743124/472357483_1876023823201095_175475186867281871_n.png?ex=677bf38e&is=677aa20e&hm=2cfb45bcb451705ddacbabb4dd447ca2cf0dc92885b9eb25e9d59bf41476ac95&=&format=webp&quality=lossless&width=400&height=225"
            ])
        }
        return responses.get(key)

async def setup(bot):
    await bot.add_cog(MessageCog(bot))

