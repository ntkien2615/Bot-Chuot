import discord
from discord.ext import commands
from discord import app_commands
import random
import asyncio


# Chương trình giả lập lại trò chơi poker 5 lá ở project cơ sở lập trình, trông nó khá xàm nhưng giả lập lại cho nhớ
from commands.base_command import FunCommand


# Chương trình giả lập lại trò chơi poker 5 lá ở project cơ sở lập trình, trông nó khá xàm nhưng giả lập lại cho nhớ
class fiveCardPoker(FunCommand):
    def __init__(self, bot):
        super().__init__(bot)
        # Card emojis for visual appeal
        self.suit_emojis = {
            'Hearts': '♥️',
            'Diamonds': '♦️',
            'Clubs': '♣️',
            'Spades': '♠️'
        }
        # Hand ranking explanation
        self.hand_descriptions = {
            'Royal Flush': 'Các lá bài cùng chất từ 10 đến A',
            'Straight Flush': 'Các lá bài cùng chất liên tiếp',
            'Four of a Kind': 'Tứ quý - 4 lá cùng giá trị',
            'Full House': 'Cù lũ - 3 lá cùng giá trị và 1 đôi',
            'Flush': 'Thùng - 5 lá cùng chất',
            'Straight': 'Sảnh - 5 lá liên tiếp',
            'Three of a Kind': 'Bộ ba - 3 lá cùng giá trị',
            'Two Pair': 'Hai đôi',
            'One Pair': 'Một đôi',
            'High Card': 'Bài cao nhất'
        }
    
    def deck(self):
        deck = []
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        for suit in suits:
            for value in values:
                deck.append(f'{value} of {suit}')
        return deck
    
    def shuffleDeck(self):
        deck = self.deck()
        random.shuffle(deck)
        return deck
    
    def dealHand(self, deck):
        hand = []
        for i in range(5):
            hand.append(deck.pop())
        return hand
    
    def format_card(self, card):
        value, _, suit = card.partition(' of ')
        return f"{value}{self.suit_emojis[suit]}"
    
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

    @app_commands.command(name='5_card_poker', description='Chơi poker 5 lá với bạn bè trong server')
    @app_commands.describe(players='Chọn người chơi (2-6 người, ví dụ: @user1 @user2)')
    async def fiveCardPoker(self, interaction: discord.Interaction, players: str):
        # Convert mentions string to list of members
        member_ids = [int(id.strip('<@!>')) for id in players.split() if id.startswith('<@')]
        members = [interaction.guild.get_member(id) for id in member_ids]
        
        # Filter out None values (invalid members)
        members = [m for m in members if m is not None]
        
        if interaction.user not in members:
            members.append(interaction.user)
        
        if len(members) < 2 or len(members) > 6:
            await interaction.response.send_message("🃏 Cần chọn từ 2 đến 6 người chơi để bắt đầu ván poker!", ephemeral=True)
            return
            
        if len(set(members)) != len(members):
            await interaction.response.send_message("⚠️ Không thể chọn trùng người chơi!", ephemeral=True)
            return

        player_mentions = " ".join(member.mention for member in members)
        await interaction.response.send_message(f"🎮 **Bắt đầu ván poker!**\nNgười chơi: {player_mentions}")
        
        # Send rules explanation
        rules_embed = discord.Embed(
            title="🃏 Luật chơi Poker 5 lá",
            description="Mỗi người chơi nhận 5 lá bài, người có bài cao nhất sẽ thắng.",
            color=discord.Color.gold()
        )
        await interaction.channel.send(embed=rules_embed)
        
        deck = self.shuffleDeck()
        hands = []
        
        # Deal cards to each player
        for _ in range(len(members)):
            hands.append(self.dealHand(deck))
        
        # Show each player's hand one card at a time
        for member, hand in zip(members, hands):
            formatted_cards = [self.format_card(card) for card in hand]
            hand_embed = discord.Embed(
                title=f"🎴 Bài của {member.display_name}",
                color=discord.Color.blue()
            )
            
            revealed_cards = []
            for card in formatted_cards:
                revealed_cards.append(card)
                hand_embed.description = " ".join(revealed_cards)
                
                reveal_message = await interaction.channel.send(embed=hand_embed)
                await asyncio.sleep(0.8)  # Slightly faster reveal
            
            # After all cards are revealed, show the hand value
            hand_value = self.handValue(hand)
            hand_embed.description = " ".join(formatted_cards)
            hand_embed.add_field(
                name="Kết quả", 
                value=f"**{hand_value}** - {self.hand_descriptions[hand_value]}"
            )
            await reveal_message.edit(embed=hand_embed)
            await asyncio.sleep(1)  # Pause before next player's reveal

        # Determine winner(s)
        winners = self.determine_winner(hands)
        result_embed = discord.Embed(
            title="🏆 Kết quả trận đấu",
            color=discord.Color.gold()
        )
        
        if len(winners) == 1:
            winner = members[winners[0]]
            winner_hand = self.handValue(hands[winners[0]])
            result_embed.description = f"**{winner.display_name}** thắng với bài **{winner_hand}**! 🎉"
            result_embed.set_thumbnail(url=winner.display_avatar.url)
        else:
            winner_names = ', '.join([members[w].display_name for w in winners])
            winner_hand = self.handValue(hands[winners[0]])
            result_embed.description = f"**Hòa!** Những người chơi sau có bài cao nhất (**{winner_hand}**):\n{winner_names}"
        
        await interaction.channel.send(embed=result_embed)

async def setup(bot):
    await bot.add_cog(fiveCardPoker(bot))