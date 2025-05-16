import discord
from discord.ext import commands
import traceback
import sys
import constants


class ErrorHandler:
    """Handles error events and logging."""
    
    def __init__(self, bot):
        self.bot = bot
        self.register_error_handlers()
    
    def register_error_handlers(self):
        @self.bot.event
        async def on_command_error(ctx, error):
            """Handle command errors."""
            if isinstance(error, commands.CommandOnCooldown):
                await ctx.send(f'Lệnh này đang trong thời gian hồi, hãy thử lại sau {error.retry_after:.2f} giây.')
            elif isinstance(error, commands.MissingRequiredArgument):
                await ctx.send(f'Thiếu tham số: {error.param.name}')
            elif isinstance(error, commands.BadArgument):
                await ctx.send(f'Tham số không đúng định dạng: {str(error)}')
            elif isinstance(error, commands.MissingPermissions):
                await ctx.send(f'Bạn không có quyền sử dụng lệnh này.')
            elif isinstance(error, commands.BotMissingPermissions):
                await ctx.send(f'Bot không có đủ quyền để thực hiện lệnh này.')
            else:
                print(f'Unhandled command error: {error}', file=sys.stderr)
                traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
        
        @self.bot.event
        async def on_error(event, *args, **kwargs):
            """Handle general Discord errors."""
            error = sys.exc_info()[1]
            error_traceback = traceback.format_exc()
            print(f'Error in event {event}: {error}\n{error_traceback}', file=sys.stderr)
    
    async def handle_interaction_error(self, interaction, error):
        """Handle application command (slash command) errors."""
        embed = discord.Embed(
            title="Đã xảy ra lỗi",
            description=str(error),
            color=constants.ERROR_EMBED_COLOR
        )
        
        if interaction.response.is_done():
            await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message(embed=embed, ephemeral=True)
        
        print(f'Interaction error: {error}', file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr) 