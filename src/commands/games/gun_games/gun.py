"""
Russian Roulette Game - Import từ module mới
"""
# Import class từ file mới
from .gun_roulette import GunRoulette

# Export cho setup function
async def setup(bot):
    await bot.add_cog(GunRoulette(bot))