import discord
from discord import Interaction
from discord.ext import commands
from discord.ui import Button, View
import asyncio


class mView(View):
    def __init__(self, msg, game):
        super().__init__()
        self.msg = msg
        self.game = game
    
    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green)
    async def Yes(self, interaction: Interaction, button):
        await interaction.response.defer()

    @discord.ui.button(label="No", style=discord.ButtonStyle.red)
    async def No(self, interaction: Interaction, button):
        await interaction.response.defer()
    
    async def on_error(self, interaction: Interaction, error: Exception, item) -> None:
        print(error)
        return await super().on_error(interaction, error, item)


class Moderation(commands.Cog):
    def __init__(self, Client):
        self.client = Client
        print("Starting Up Moderation")

    @commands.command()
    async def purge(self, ctx, limit: int):
        await ctx.channel.purge(limit=limit+1)
        
    @commands.command()
    async def timeout(self, ctx):
        embed = discord.Embed(title="Timeout Vote", color=0xFF5733)
        pass

async def setup(client):
    await client.add_cog(Moderation(client))