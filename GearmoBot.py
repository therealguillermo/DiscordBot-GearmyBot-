import discord
from discord.ext import commands
import asyncio
import faceitFinder
import musicPlayer
#import FlightRadar
import Gamble
import Chat
import Moderation
import minecraftServer
from api_keys import APIKEY

BOT_TOKEN = APIKEY.getKey('bot_token')

intents = discord.Intents().all()
intents.members = True
intents.message_content = True
intents.voice_states = True

client = commands.Bot(command_prefix="?", intents=intents)

# musicPlayer.setup(client) #pylint ignore
# faceitFinder.setup(client) #pylint ignore
# Gamble.setup(client) #pylint ignore

async def load_cogs():
    await musicPlayer.setup(client)
    await Gamble.setup(client)
    #await FlightRadar.setup(client)
    #await faceitFinder.setup(client)
    #await Chat.setup(client)
    await Moderation.setup(client)
    await MinecraftServer.setup(client)
    print("Successfully loaded all cogs")

async def main():
    async with client:
        await load_cogs()
        await client.start(BOT_TOKEN)

asyncio.run(main())