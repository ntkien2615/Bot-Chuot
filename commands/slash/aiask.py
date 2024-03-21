import discord
from discord.ext import commands
import google.generativeai as genai
from discord import app_commands

ai_key = open('./secret/ai_api_key.txt',"r")
ai_key = ai_key.read()
genai.configure(api_key="AIzaSyBGNNWVKA27-Trq2tuK7IGPFqFwqZP8PeQ")
model = genai.GenerativeModel('models/gemini-pro',safety_settings=[
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}])

class aiask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name='aiask', description='Hỏi AI')
    @app_commands.describe(question='bạn hỏi cái gì')
    async def aiask(self, interaction:discord.Interaction, question:str):
      try:       
        reply = model.generate_content(f"{question}")
        reply = reply.text
        embed = discord.Embed(title="AI ASK", description=question, color=discord.Color.random())
        embed.add_field(name="", value=f"{reply}", inline=False)
        await interaction.response.send_message(embed=embed)
      except Exception as e:
            print(e)

async def setup(bot):
  await bot.add_cog(aiask(bot))
