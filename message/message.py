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
            dead_chat_ans = ['dead cc','Dead mả cha m nhé']
            await message.channel.send(random.choice(dead_chat_ans))
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
                await message.reply('Về bot chuột. Bot chuột là con bot rất láo và ổn lào, và bạn gõ slash /info đấy dumb, tao không hiểu tại sao thằng kia nó lại làm cái này, bot có lệnh slash hết rồi')
                await self.bot.process_commands(message)
        
        kevin = ['kevin', 'kê vin']
        for kevin_word in kevin:
            if kevin_word in message.content.lower():
                await message.reply('<@868475751459094580>')
                await self.bot.process_commands(message)
                
        pholotino = ['florentino', 'fo lon ti no', 'pholotino']
        for pholotino_word in pholotino:
            if pholotino_word in message.content.lower():
                await message.reply('Không biết anh Thành Vũ có biết Tú có Ny hay không😗😗 chúng tôi biết rằng tú có ny là người chơi khá nổi tiếng với con bài Florentino😲😲 ngày hôm nay anh ta đi cầm Florentino và chơi rất hay😎 trận thi đấu vừa xong là trận thi đấu mà chúng ta có thể thấy rằng là các bạn khán giả cũng có kĩ năng rất tốt- đặc biệt là người chơi bên phía của đội tuyển Đồng 5 đội tuyển Trái Đất đó là Tú có Ny🥳 tôi thấy rằng anh ta chưa để cái tốc biến mình hồi được hiện xanh quá lâu anh ta sử dụng ngay lập tức bằng những tình huống mở giao tranh của mình và chính Tú có Ny là MVP của trận thi đấu này với 14.0 điểm MVP😎😎. Một tình huống mà có lẽ Flo đang làm quá nhiều điều🤕🤕 những tình huống bông muq muq muq muq, bỏ chạy với Flo, Flo đang múa quá nhức nách, phải nói là Flo võ công quá cao cường🔪🔪😏😏. Và đây là Florentino, Florentino ui 🥶🥶👿👿😳một cái tình huống phải nói là cực gắt.👿Tú có Ny và người chơi này có lẽ sẽ có Ny thôi🥴🥴đánh quá ghê. Những tình huống bông hoa bông hủng phải nói là đúng top 1, buff bẩn🥵🥵. Quá ghê gớm....🌚😳 Và đây là Folontilô!😱😱 Folontilô ui... 🥶🥶👿😳một tình huống múa phải nói là cực 👿gắt!! *music🤯 Thẹn thùng nhìn em quay gót đi mãi😞😞💔 Anh đứng chết lặng trong mưa😭😭 Dù rằng bên😊😊 em đã có ai Nhưng nơi đây anh 🤗🤗🥱vẫn còn chờ...')
                await self.bot.process_commands(message)

        jack = ['jack'," trịnh trần phương tuấn",'j97','trinh tran phuong tuan','meo meo','5 củ','jack bến tre']
        jack_ans = [
            'Idol tôi là JACK đó rồi sao 🙂? Đối với những người ghét JACK,ĐÓM chúng tôi là Ruồi đó rồi sao 🙂? Liên quan gì ? Tôi nói idol tôi đẹp chứ đâu phải mấy người nói đâu ? Ủa bị gì vậy? Những người fan JACK cũng đều bị anti mấy người chửi đó ? Không liên quan lắm nhưng mà chuyện cuat người ta xía mồm vào làm gì ? Rảnh quá đi soi chuyện người khác có thấy trẻ con quá không?Lúc JACK chưa lên tiếng gì cả thì cũng bu vào xỉ xó giờ JACK lên tiếng rồi thì cũng xỉ xó bu vào phẫn nộ bài viết.rồi làm vậy có ích gì? Có tốt lành gì không? Rồi những người nổi tiếng khác cũng là fan ẢNH vào cmt tus ẢNH cũng bay vô chửi họ ? Ủa rồi người mình ngưỡng mộ fan người mình anti rồi tức bay vào chửi à ? Nói này nói nọ bảo “Thiếu fame” ủa thiếu fane là thiếu fame làm sao? Ủa tự nhiên fan anh JACK cái bảo thiếu fame rảnh vừa thôi chứ? Vào group của ĐÓM rồi vào từng bài viết chửi ? Ủa làm vậy để cho người khác ghét mình hơn à? Mấy người là anti thì có liên quan gì tới người mà mình anti không mà bu vào chửi ? nói chung là We’re no strangers to love, You know the rules and so do I. A full commitment’s what I’m thinking of You wouldnt get this from any other guy. I just wanna tell you how I’m feeling, Gotta make you understand... Never gonna give you up, Never gonna let you down, Never gonna run around and desert you.',
            'Đừnq 👐 bao zờ 😏 gkét 😡 a Jack 😢😭, đom đóm 👉 củg zậy 😉đừg 🤫 bao zờ 😠 gkét 🤬 a ♥️😍😍 đom đóm xẽ 🙂 trịu hớt 🤯 trịu hớt😣😵 ta^t kả😇 la j fan😔 đừg lam 😠 a Jack🤩 tổn tkưg 😭😭 đom đóm xẽ đau 🙁 nkư dao kắt 🔪🔪 kim đăm 💔💔Đừnq 👐 bao zờ 😏 gkét 😡 a Jack 😢😭, đom đóm 👉 củg zậy 😉đừg 🤫 bao zờ 😠 gkét 🤬 a ♥️😍😍 đom đóm xẽ 🙂 trịu hớt 🤯 trịu hớt😣😵 ta^t kả😇 la j fan😔 đừg lam 😠 a Jack🤩 tổn tkưg 😭😭 đom đóm xẽ đau 🙁 nkư dao kắt 🔪🔪 kim đăm 💔💔Đừnq 👐 bao zờ 😏 gkét 😡 a Jack 😢😭, đom đóm 👉 củg zậy 😉đừg 🤫 bao zờ 😠 gkét 🤬 a ♥️😍😍 đom đóm xẽ 🙂 trịu hớt 🤯 trịu hớt😣😵 ta^t kả😇 la j fan😔 đừg lam 😠 a Jack🤩 tổn tkưg 😭😭 đom đóm xẽ đau 🙁 nkư dao kắt 🔪🔪 kim đăm 💔💔'
        ]
        for jack_word in jack:
            if jack_word in message.content.lower():
                await message.reply(random.choice(jack_ans))
                
async def setup(bot):
    await bot.add_cog(on_message(bot))
