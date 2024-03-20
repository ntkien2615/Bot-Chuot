import discord
from discord.ext import commands
import google.generativeai as genai
from discord import app_commands

ai_key = open('./secret/ai_api_key.txt',"r")
ai_key = ai_key.read()
genai.configure(api_key=ai_key)

model = genai.GenerativeModel('gemini-pro',safety_settings=[
{
  "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT"
  "probability": "NEGLIGIBLE"
},
{
  "category": "HARM_CATEGORY_HATE_SPEECH"
  "probability": "NEGLIGIBLE"
},
{
  "category": "HARM_CATEGORY_HARASSMENT"
  "probability": "NEGLIGIBLE"
},
{
  "category": "HARM_CATEGORY_DANGEROUS_CONTENT"
  "probability": "NEGLIGIBLE"
}
])


class AiAsk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="AIask",description="Hỏi người máy")
    @app_commands.describe(search='bạn hỏi cái gì')
    async def AiAsk(self, interaction:discord.Interaction, search:str):
        response = model.generate_content(prompt)
        await interaction.response.send_message(response.text)

        

    
    

def setup(bot):
    bot.add_cog(AiAsk(bot))
