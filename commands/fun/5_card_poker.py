import discord
from discord.ext import commands
from discord import app_commands
import random
import asyncio

class fiveCardPoker(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    def deck(self):
        deck = []
        for i in range(4):
            for j in range(2,15):
                deck.append(j,i)
                return deck
    
    def shuffleDeck(self):
        deck = self.deck()
        random.shuffle(deck)
        return deck
    
    