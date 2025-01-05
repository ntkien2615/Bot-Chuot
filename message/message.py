from discord.ext import commands
import random
import discord

class on_message(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def message(self, message):
        if message.author.bot:
            return
        await self.bot.process_commands(message)

        responses = {
            'hi': ['chào', 'hi', 'hello', 'chao', 'xin chào', 'xin chao'],
            'bye': ['bye'],
            'dead_chat': ['dead chat', 'dead chat xd', 'dead chat guys'],
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

        for key, words in responses.items():
            if any(word in message.content.lower() for word in words):
                if key == 'hi':
                    await message.channel.send('chào cc')
                elif key == 'bye':
                    await message.channel.send('sủi cmm luôn đi')
                elif key == 'dead_chat':
                    dead_chat_ans = ['dead cc', 'Dead mả cha m nhé']
                    await message.channel.send(random.choice(dead_chat_ans))
                elif key == 'russian':
                    await message.channel.send('NO RUSSIAN')
                elif key == 'ukrainian':
                    await message.add_reaction("🤡")
                elif key == 'sui':
                    await message.channel.send(f'{message.author.display_name} *sẽ im lặng và biến mất...*')
                elif key == 'dmcs':
                    await message.reply(f'{message.author.display_name}')
                    await message.channel.send("https://th.bing.com/th/id/R.2f1a48275690965a28da2930ea9d85dd?rik=%2fu7q7c6PPfn6wA&pid=ImgRaw&r=0")
                elif key == 'non':
                    await message.channel.send('Êu, có con gà non chưa kìa')
                elif key == 'ngot':
                    await message.reply('cẩn thận bị tiểu đường')
                elif key == 'overthinking':
                    await message.reply("Why we overthinking when we can ||Ov3Rdo$$3||. :3")
                elif key == 'about':
                    await message.reply('Về bot chuột. Bot chuột là con bot rất láo và ổn lào, và bạn gõ slash /info đấy dumb, tao không hiểu tại sao thằng kia nó lại làm cái này, bot có lệnh slash hết rồi')
                elif key == 'kevin':
                    await message.reply('<@868475751459094580>')
                elif key == 'pholotino':
                    await message.reply('Không biết anh Thành Vũ có biết Tú có Ny hay không😗😗 chúng tôi biết rằng tú có ny là người chơi khá nổi tiếng với con bài Florentino😲😲 ngày hôm nay anh ta đi cầm Florentino và chơi rất hay😎 trận thi đấu vừa xong là trận thi đấu mà chúng ta có thể thấy rằng là các bạn khán giả cũng có kĩ năng rất tốt- đặc biệt là người chơi bên phía của đội tuyển Đồng 5 đội tuyển Trái Đất đó là Tú có Ny🥳 tôi thấy rằng anh ta chưa để cái tốc biến mình hồi được hiện xanh quá lâu anh ta sử dụng ngay lập tức bằng những tình huống mở giao tranh của mình và chính Tú có Ny là MVP của trận thi đấu này với 14.0 điểm MVP😎😎. Một tình huống mà có lẽ Flo đang làm quá nhiều điều🤕🤕 những tình huống bông muq muq muq muq, bỏ chạy với Flo, Flo đang múa quá nhức nách, phải nói là Flo võ công quá cao cường🔪🔪😏😏. Và đây là Florentino, Florentino ui 🥶🥶👿👿😳một cái tình huống phải nói là cực gắt.👿Tú có Ny và người chơi này có lẽ sẽ có Ny thôi🥴🥴đánh quá ghê. Những tình huống bông hoa bông hủng phải nói là đúng top 1, buff bẩn🥵🥵. Quá ghê gớm....🌚😳 Và đây là Folontilô!😱😱 Folontilô ui... 🥶🥶👿😳một tình huống múa phải nói là cực 👿gắt!! *music🤯 Thẹn thùng nhìn em quay gót đi mãi😞😞💔 Anh đứng chết lặng trong mưa😭😭 Dù rằng bên😊😊 em đã có ai Nhưng nơi đây anh 🤗🤗🥱vẫn còn chờ...')
                elif key == 'jack':
                    jack_ans = [
                        'Idol tôi là JACK đó rồi sao 🙂? Đối với những người ghét JACK,ĐÓM chúng tôi là Ruồi đó rồi sao 🙂? Liên quan gì ? Tôi nói idol tôi đẹp chứ đâu phải mấy người nói đâu ? Ủa bị gì vậy? Những người fan JACK cũng đều bị anti mấy người chửi đó ? Không liên quan lắm nhưng mà chuyện cuat người ta xía mồm vào làm gì ? Rảnh quá đi soi chuyện người khác có thấy trẻ con quá không?Lúc JACK chưa lên tiếng gì cả thì cũng bu vào xỉ xó giờ JACK lên tiếng rồi thì cũng xỉ xó bu vào phẫn nộ bài viết.rồi làm vậy có ích gì? Có tốt lành gì không? Rồi những người nổi tiếng khác cũng là fan ẢNH vào cmt tus ẢNH cũng bay vô chửi họ ? Ủa rồi người mình ngưỡng mộ fan người mình anti rồi tức bay vào chửi à ? Nói này nói nọ bảo “Thiếu fame” ủa thiếu fane là thiếu fame làm sao? Ủa tự nhiên fan anh JACK cái bảo thiếu fame rảnh vừa thôi chứ? Vào group của ĐÓM rồi vào từng bài viết chửi ? Ủa làm vậy để cho người khác ghét mình hơn à? Mấy người là anti thì có liên quan gì tới người mà mình anti không mà bu vào chửi ? nói chung là We’re no strangers to love, You know the rules and so do I. A full commitment’s what I’m thinking of You wouldnt get this from any other guy. I just wanna tell you how I’m feeling, Gotta make you understand... Never gonna give you up, Never gonna let you down, Never gonna run around and desert you.',
                        'Đừnq 👐 bao zờ 😏 gkét 😡 a Jack 😢😭, đom đóm 👉 củg zậy 😉đừg 🤫 bao zờ 😠 gkét 🤬 a ♥️😍😍 đom đóm xẽ 🙂 trịu hớt 🤯 trịu hớt😣😵 ta^t kả😇 la j fan😔 đừg lam 😠 a Jack🤩 tổn tkưg 😭😭 đom đóm xẽ đau 🙁 nkư dao kắt 🔪🔪 kim đăm 💔💔Đừnq 👐 bao zờ 😏 gkét 😡 a Jack 😢😭, đom đóm 👉 củg zậy 😉đừg 🤫 bao zờ 😠 gkét 🤬 a ♥️😍😍 đom đóm xẽ 🙂 trịu hớt 🤯 trịu hớt😣😵 ta^t kả😇 la j fan😔 đừg lam 😠 a Jack🤩 tổn tkưg 😭😭 đom đóm xẽ đau 🙁 nkư dao kắt 🔪🔪 kim đăm 💔💔Đừnq 👐 bao zờ 😏 gkét 😡 a Jack 😢😭, đom đóm 👉 củg zậy 😉đừg 🤫 bao zờ 😠 gkét 🤬 a ♥️😍😍 đom đóm xẽ 🙂 trịu hớt 🤯 trịu hớt😣😵 ta^t kả😇 la j fan😔 đừg lam 😠 a Jack🤩 tổn tkưg 😭😭 đom đóm xẽ đau 🙁 nkư dao kắt 🔪🔪 kim đăm 💔💔'
                    ]
                    await message.reply(random.choice(jack_ans))
                elif key == 'link':
                    await message.reply('https://media.discordapp.net/attachments/883268139922636820/1287350064276045824/278755226_745698233463800_1291647474017004061_n.png?ex=66f139ad&is=66efe82d&hm=691315948a3b26a3d54e02820608b560bba49b35bf5b5c7b6812774e01660bd5&=&format=webp&quality=lossless&width=200&height=252')
                elif key == 'thai_land':
                    await message.reply('Ăn lẩu cay 5-3')

async def setup(bot):
    await bot.add_cog(on_message(bot))
