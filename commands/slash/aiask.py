import discord, os
from discord.ext import commands
import google.generativeai as genai
from discord import app_commands
from dotenv import load_dotenv, find_dotenv


class aiask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name='aiask', description='Hỏi AI')
    @app_commands.describe(question='bạn hỏi cái gì')
    async def aiask(self, interaction:discord.Interaction, question:str):      
        if not question or len(question) > 200:
            await interaction.response.send_message("Câu hỏi không hợp lệ.")
            return
        
        load_dotenv(find_dotenv())
        ai_api_key = os.getenv("ai_api_key")
        genai.configure(api_key=ai_api_key)
        model = genai.GenerativeModel('gemini-pro',safety_settings=[
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ])

        try:
            reply = await model.generate_content(question)
        except Exception as e:
            print(f"Lỗi khi gọi API: {e}")
            await interaction.response.send_message("Lỗi hệ thống. Vui lòng thử lại sau.")
            return

        await interaction.response.send_message(f'{reply.text}')

async def setup(bot):
  await bot.add_cog(aiask(bot))
