import discord, os
from discord.ext import commands
import google.generativeai as genai
from discord import app_commands
from dotenv import load_dotenv, find_dotenv
from src.commands.base_command import SlashCommand

class AiAskCommand(SlashCommand):
    """Command to ask questions to AI assistant."""
    
    category = "utility"  # This will be used by the help command
    
    def __init__(self, discord_bot):
        super().__init__(discord_bot)
        self.name = "aiask"
        self.description = "Hỏi AI assistant"
        
        # Initialize AI configuration once during startup
        load_dotenv(find_dotenv())
        self.ai_api_key = os.getenv("ai_api_key")
        if self.ai_api_key:
            genai.configure(api_key=self.ai_api_key)
            self.model = genai.GenerativeModel('gemini-pro', safety_settings=[
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            ])
    
    async def execute(self, interaction, question):
        """Execute the aiask command."""
        if not question:
            await interaction.response.send_message("Vui lòng nhập câu hỏi.")
            return
            
        if len(question) > 200:
            await interaction.response.send_message("Câu hỏi không được vượt quá 200 ký tự.")
            return
        
        if not self.ai_api_key:
            await interaction.response.send_message("API key chưa được cấu hình.")
            return

        # Show typing indicator while processing
        await interaction.response.defer()

        try:
            reply = self.model.generate_content(question)
            reply_text = reply.text

            # Handle long responses
            if len(reply_text) > 2000:
                reply_text = reply_text[:1997] + "..."

            await interaction.followup.send(reply_text)
            
        except Exception as e:
            print(f"Lỗi khi gọi API: {e}")
            await interaction.followup.send("Có lỗi xảy ra khi xử lý câu hỏi. Vui lòng thử lại sau.")
    
    async def register_slash_command(self):
        """Register the aiask slash command."""
        pass  # Handled by Discord.py's decorator system
    
    @app_commands.command(name='aiask', description='Hỏi AI assistant')
    @app_commands.describe(question='bạn hỏi cái gì')
    async def aiask(self, interaction: discord.Interaction, question: str):
        await self.execute(interaction, question)
