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
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        for suit in suits:
            for value in values:
                deck.append(f'{value} of {suit}')
        return deck  # Add return statement
    
    def shuffleDeck(self):
        deck = self.deck()
        random.shuffle(deck)
        return deck
    
    def dealHand(self, deck):
        hand = []
        for i in range(5):
            hand.append(deck.pop())
        return hand
    
    def handValue(self, hand):
        values = []
        suits = []
        for card in hand:
            values.append(card.split()[0])
            suits.append(card.split()[2])
        values.sort()
        if values == ['10', 'J', 'Q', 'K', 'A'] and len(set(suits)) == 1:
            return 'Royal Flush'
        if len(set(suits)) == 1 and values == ['2', '3', '4', '5', 'A']:
            return 'Straight Flush'
        if len(set(values)) == 2:
            if values.count(values[0]) in [1, 4]:
                return 'Four of a Kind'
            return 'Full House'
        if len(set(suits)) == 1:
            return 'Flush'
        if values == ['2', '3', '4', '5', 'A']:
            return 'Straight'
        if len(set(values)) == 3:
            if values.count(values[0]) in [1, 3]:
                return 'Three of a Kind'
            return 'Two Pair'
        if len(set(values)) == 4:
            return 'One Pair'
        return 'High Card'
    
    def determine_winner(self, hands):
        hand_rankings = {
            'Royal Flush': 10,
            'Straight Flush': 9,
            'Four of a Kind': 8,
            'Full House': 7,
            'Flush': 6,
            'Straight': 5,
            'Three of a Kind': 4,
            'Two Pair': 3,
            'One Pair': 2,
            'High Card': 1
        }
        best_value = 0
        winners = []
        for i, hand in enumerate(hands):
            current_value = hand_rankings[self.handValue(hand)]
            if current_value > best_value:
                best_value = current_value
                winners = [i]
            elif current_value == best_value:
                winners.append(i)
        return winners

    @app_commands.command(name='5_card_poker', description='poker 5 lá với người chơi trong server')
    @app_commands.describe(players='Chọn người chơi (2-6 người)')
    async def fiveCardPoker(self, interaction: discord.Interaction, players: str):
        # Convert mentions string to list of members
        member_ids = [int(id.strip('<@!>')) for id in players.split() if id.startswith('<@')]
        members = [interaction.guild.get_member(id) for id in member_ids]
        
        # Filter out None values (invalid members)
        members = [m for m in members if m is not None]
        
        if len(members) < 2 or len(members) > 6:
            await interaction.response.send_message("Cần chọn từ 2 đến 6 người chơi!", ephemeral=True)
            return
            
        if len(set(members)) != len(members):
            await interaction.response.send_message("Không thể chọn trùng người chơi!", ephemeral=True)
            return

        player_mentions = " ".join(member.mention for member in members)
        await interaction.response.send_message(f"Bắt đầu ván poker với {player_mentions}!")
        
        deck = self.shuffleDeck()
        hands = []
        
        # Deal cards to each player
        for _ in range(len(members)):
            hands.append(self.dealHand(deck))
        
        # Show each player's hand
        for member, hand in zip(members, hands):
            await interaction.channel.send(f"{member.mention}: {', '.join(hand)} - {self.handValue(hand)}")
        
        # Determine winner(s)
        winners = self.determine_winner(hands)
        if len(winners) == 1:
            winner = members[winners[0]]
            await interaction.channel.send(
                f"{winner.mention} thắng với bài {self.handValue(hands[winners[0]])}!"
            )
        else:
            winner_mentions = ', '.join([members[w].mention for w in winners])
            await interaction.channel.send(
                f"Hòa! Những người chơi sau có bài cao nhất: {winner_mentions}"
            )

async def setup(bot):
    await bot.add_cog(fiveCardPoker(bot))  # Fix cog addition