import discord
from discord.ext import commands
from gamblingModules.economy import Economy
from gamblingModules.blackjack import BlackJack
import random
import asyncio

class Gamble(commands.Cog):
    def __init__(self, Client):
        self.client = Client
        self.econ = Economy()
        self.blackJackGames = []
        self.client.loop.create_task(self.startEconUpdater())
        print("Starting Up Gambling")

    @commands.command()
    async def register(self, ctx):
        if self.econ.create(ctx.author):
            await ctx.send("Success!")
        else:
            await ctx.send("You're already registered")
    
    @commands.command()
    async def blackjack(self, ctx, bet=None):
        # check for error handling numbers
        print(type(ctx))
        if not bet:
            await ctx.send(f"Fucking oaf fuckin Retard I need coins")
            return
        await BlackJack.build(ctx, bet, self.econ)

    @commands.command()
    async def cf(self, ctx, credits=None):
        if not credits:
            await ctx.send(f"Fucking oaf fuckin Retard I need coins")
            return
        try:
            coins = float(credits)
        except:
            await ctx.send(f"Fucking oaf fuckin Retard I need coins not \"{credits}\"")
            return 
        sender = str(ctx.author)
        roll = random.randint(1, 100)
        amountChange = coins * 2
        if roll <= 50:
            await ctx.send(f"You have won {coins} coins")
            self.econ.addCoins(sender, coins)
        else:
            await ctx.send(f"You lost {coins} coins cunnt")
            self.econ.subCoins(sender, coins)


    #econ commands and funcs

    @commands.command()
    async def saveEconState(self,ctx):
        self.econ.save()
        await ctx.send("saved")

    @commands.command()
    async def econStatus(self, ctx):
        await ctx.send(self.econ.econ)

    @commands.command()
    async def coins(self, ctx):
        sender = str(ctx.author)
        coins = self.econ.get(sender)
        if coins.is_integer():
            coins = int(coins)
        await ctx.send(f"You have {coins} coins")

    async def startEconUpdater(self):
        while True:
            channels = self.client.get_all_channels()
            for channel in channels:
                if type(channel) == discord.channel.VoiceChannel:
                    self.econ.pump(channel.members) if channel.members != [] else None
                    
            print(f"\nDistributed\n\n\n")
            await asyncio.sleep(90)


async def setup(client):
    await client.add_cog(Gamble(client))