from logging import exception
import discord
from discord import Interaction
from discord.ext import commands
from discord.ui import Button, View
import pydealer
import asyncio


cardValues = {
    'A': 11,
    "K": 10,
    "Q": 10,
    "J": 10
}
def getCardValue(sCard, isLow=False):
    card = str(sCard)
    if card[0].isnumeric() and card[1].isnumeric():
        return int(card[:2])
    elif card[0].isnumeric():
        return int(card[0])
    else:
        if isLow:
            return 1
        else:
            return cardValues[card[0]]


class BlackJack(object):
    def __init__(self, ctx, econ):
        self.ctx = ctx
        self.bet = 0
        self.econ = econ
        self.deck = pydealer.Deck()
        self.deck.shuffle()
        self.pCards = [self.deck.deal(1), self.deck.deal(1)]
        self.dCards = [self.deck.deal(1), self.deck.deal(1)]
        self.pTotal = sum([getCardValue(i) for i in self.pCards])
        self.dTotal = sum([getCardValue(i) for i in self.dCards])
        self.stayed = False
        self.lost = False
        self.bust = False
        self.won = False
        self.tie = False
        self.blackjack = False if self.pTotal != 21 else True
    
    @classmethod
    async def build(self, ctx, bet, econ):
        self = BlackJack(ctx, econ)
        self.bet = int(bet)
        self.embed = self.build_embed()
        self.msg = await self.ctx.send(embed=self.embed)
        self.view = mView(self.msg, self)
        if self.blackjack: 
            asyncio.sleep(1)
        await self.msg.edit(embed=self.embed, view=self.view) 

    async def update(self):
        self.embed = self.build_embed()
        await self.msg.edit(embed=self.embed, view=self.view)
        if self.lost or self.bust or self.won or self.blackjack or self.tie:
            if self.lost or self.bust:
                self.econ.subCoins(str(self.ctx.author), self.bet)
            elif self.won or self.blackjack:
                self.econ.addCoins(str(self.ctx.author), self.bet)
            else:
                pass
            await asyncio.sleep(2)
            self.embed = self.build_embed(True)
            await self.msg.edit(embed=self.embed, view=None)

    def build_embed(self, final=False):
        if final:
            embed = discord.Embed()
        else:
            embed = discord.Embed(title="BlackJack", color=0xFF5733)
        intList = [str(getCardValue(i)) for i in self.pCards]
        pTotalStr = " \u200b \u200b ".join(intList)
        if self.stayed:
            dealerList = [str(getCardValue(i)) for i in self.dCards]
            dTotalStr = " \u200b \u200b ".join(dealerList)
        else:
            dTotalStr = "? \u200b \u200b " + str(getCardValue(self.dCards[1]))
        if self.won:
            betLabel = f"You Won!"
            betValue = f"You won {self.bet * 2} coins"
        elif self.blackjack:
            betLabel = f"BlackJack!"
            betValue = f"You won {self.bet * 2} coins"
        elif self.bust:
            betLabel = f"Bust!"
            betValue = f"You lost {self.bet} coins"
        elif self.lost:
            betLabel = f"You Lost!"
            betValue = f"You lost {self.bet} coins"
        elif self.tie: 
            betLabel = f"Tie!"
            betValue = f"You recieved {self.bet} coins"
        else:
            betLabel = f"Your Bet:"
            betValue = f"{self.bet}"
        if final:
            betValue += f"\nYou now have {self.econ.get(str(self.ctx.author))} coins"
        if not final:
            embed.add_field(name=f"You | {self.pTotal}", value=f"{pTotalStr}", inline=False)
            embed.add_field(name=f"Dealer | {self.dTotal}" if self.stayed or self.won else f"Dealer | ?", value=f"{dTotalStr}", inline=False)
        embed.add_field(name=betLabel, value=betValue)
        return embed

    async def hit(self):
        card = self.deck.deal(1)
        self.pCards.append(card)
        if self.pTotal + getCardValue(card) > 21 and str(card)[0] == 'A':
            self.pTotal += getCardValue(card, True)
        else:
            self.pTotal += getCardValue(card)
        if self.pTotal > 21:
            await self.update()
            await asyncio.sleep(1)
            self.bust = True
        if self.pTotal == 21:
            self.blackjack = True
        await self.update()

    async def dealerPlay(self):
        while self.dTotal < 17:
            await asyncio.sleep(1)
            card = self.deck.deal(1)
            self.dCards.append(card)
            if self.dTotal + getCardValue(card) > 21 and str(card)[0] == 'A':
                self.dTotal += getCardValue(card, True)
            else:
                self.dTotal += getCardValue(card)
            await self.update()
    
    async def stay(self):
        self.stayed = True
        await self.update()
        if self.pTotal > self.dTotal:
            await self.dealerPlay()
        await asyncio.sleep(1)
        if self.dTotal > 21:
            self.won = True
        elif self.pTotal > self.dTotal:
            self.won = True
        elif self.pTotal < self.dTotal:
            self.lost = True
        elif self.pTotal == self.pTotal:
            self.tie = True
        await self.update()
        

    async def doubleDown(self):
        pass

class mView(View):
    def __init__(self, msg, game):
        super().__init__()
        self.msg = msg
        self.game = game
    
    @discord.ui.button(label="Hit", style=discord.ButtonStyle.green)
    async def hit(self, interaction: Interaction, button):
        await interaction.response.defer()
        await self.game.hit()

    @discord.ui.button(label="Stay", style=discord.ButtonStyle.red)
    async def stay(self, interaction: Interaction, button):
        await interaction.response.defer()
        await self.game.stay()
    
    async def on_error(self, interaction: Interaction, error: Exception, item) -> None:
        print(error)
        return await super().on_error(interaction, error, item)