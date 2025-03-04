from discord.ext import commands
import random
import time

class SubMessageCog(commands.Cog):  # Changed class name

    def __init__(self, bot):
        self.bot = bot
        self.processed_messages = set()
        self.message_timestamps = {}
        self.cleanup_interval = 3600  # 1 hour
        self.last_cleanup = time.time()
        self.consecutive_message_count = {}
        self.responses_dict = {
            'gay': ['Thằng vừa nhắn "Gay" là gay và rất thích xem kumalala, thug hunter, ambatukam, boku no pico, và các thể loại khác']
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
                "gay": ['gay', 'gаy']
            }

            message_content = message.content.lower()
            for key, keywords in responses.items():
                if any(keyword in message_content for keyword in keywords):
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
    await bot.add_cog(SubMessageCog(bot))  # Updated to use new class name
