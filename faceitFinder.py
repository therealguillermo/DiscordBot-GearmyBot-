import discord
from discord.ext import commands
from faceit_api.faceit_data import FaceitData
from faceitFinderModules.faceitPlayer import faceitPlayer
import asyncio
from api_keys import APIKEY

FACEITAPIKEY = APIKEY.getKey('faceit')

class faceitFinder(commands.Cog):
    def __init__(self, Client):
        self.client = Client
        self.faceitAPI = FaceitData(FACEITAPIKEY)
        print("Starting Up faceitFinder")

    @commands.command()
    async def faceit(self, ctx, URL, is20=''):
        err = True
        if is20.lower() == 'true':
            is20 = True
        else:
            is20 = False
        if is20:
            msg = await ctx.send("Gathering Faceit Data for last 20 matches...")
        try:
            player = faceitPlayer(self.faceitAPI, URL, is20)
            err = False
        except Exception as e:
            print(e)
            await ctx.send("Could not find faceit from URL")
        if is20:
            await msg.delete()
        if not err:
            sEmbed = await self.embed(player, is20) 
            await ctx.send(embed=sEmbed)
        

    async def embed(self, faceitPlayer, is20):
        embed = discord.Embed(title="Faceit", url=faceitPlayer.url, color=0xFF5733) #can be information about the player
        embed.set_author(name=faceitPlayer.nickname, url=faceitPlayer.url, icon_url=faceitPlayer.avatar) # this will be faceit player img and username
        embed.set_thumbnail(url=faceitPlayer.levelIMG) #level picture here
        #matches
        embed.add_field(name="Matches", value=faceitPlayer.matches, inline=True)
        #winrate
        embed.add_field(name="Win Rate %", value=f"{faceitPlayer.WRp}%", inline=True)
        #elo
        embed.add_field(name="Elo", value=faceitPlayer.elo)
        #longest winstreak
        embed.add_field(name="Longest Win Streak", value=faceitPlayer.winStreak, inline=True)
        #average kd
        embed.add_field(name="K/D Ratio", value=faceitPlayer.kd, inline=True)
        #average HS's
        embed.add_field(name="Average HS %", value=f"{faceitPlayer.HSp}%", inline=True)
        #last 20 matches
        if is20:
            #titles for last 20 matches
            embed.add_field(name="\u200b\n-- Last 20 match stats --", value="\u200b", inline=False)
            #average kills
            embed.add_field(name="Average Kills", value=f"{faceitPlayer.kills20}", inline=True)
            #average kd
            embed.add_field(name="Average K/D", value=f"{faceitPlayer.KD20}", inline=True)
            #average kr
            embed.add_field(name="Average K/R", value=f"{faceitPlayer.KR20}", inline=True)
            #average hs
            embed.add_field(name="Average HS", value=f"{faceitPlayer.HS20}", inline=True)
            #first half of games as list
            embed.add_field(name="Recent Matches", value=f"{faceitPlayer.games}", inline=True)
            #second half of games as list
            embed.add_field(name="\u200b", value=f"{faceitPlayer.games2}", inline=True)
        return embed


async def setup(client):
    await client.add_cog(faceitFinder(client))

    