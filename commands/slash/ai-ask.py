import discord
from discord.ext import commands
import google.generativeai as genai
from discord import app_commands

ai_key = open('./secret/ai_api_key.txt',"r")
ai_key = ai_key.read()
genai.configure(api_key=ai_key)

model = genai.GenerativeModel('gemini-pro',safety_settings=[
{
  "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
  "threshold": "BLOCK_NONE",
},
{
  "category": "HARM_CATEGORY_HATE_SPEECH",
  "threshold": "BLOCK_NONE",
},
{
  "category": "HARM_CATEGORY_HARASSMENT",
  "threshold": "BLOCK_NONE",
},
{
  "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
  "threshold": "BLOCK_NONE",
}
])


class aiAsk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="aiask",description="Hỏi người máy")
    @app_commands.describe(question='bạn hỏi cái gì')
    async def aiask(self, interaction:discord.Interaction, question:str):
      reply = model.generate_content(f"{question}")
      await interaction.response.send_message(f"{reply.text}")

def setup(bot):
    bot.add_cog(aiAsk(bot))
