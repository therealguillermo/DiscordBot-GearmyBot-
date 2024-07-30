import discord
from discord.ext import commands
import os
import subprocess
import asyncio

MC_SERVER_PATH = '/home/opc/ATM6-1.9.2-server'
START_SCRIPT = os.path.join(MC_SERVER_PATH, 'startserver.sh')
TMUX_SESSION_NAME = 'mc'

class MinecraftServer(commands.Cog):
    def __init__(self, Client):
        self.client = Client
        self.start_script = START_SCRIPT
        self.tmux_session_name = TMUX_SESSION_NAME
        self.output_displaying = False

    def is_running(self):
        result = subprocess.run(
            ['tmux', 'has-session', '-t', self.tmux_session_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return result.returncode == 0

    @commands.command()
    async def start(self, ctx, *args):
        if self.is_running():
            ctx.send("Minecraft server is already running in tmux.")
            return "Minecraft server is already running in tmux."
        else:
            subprocess.run(
                ['tmux', 'new-session', '-d', '-s', self.tmux_session_name, 'sh', self.start_script]
            )
            await ctx.send("Minecraft server started in tmux.")
            return "Minecraft server started in tmux."

    @commands.command()
    async def stop(self, ctx, *args):
        if self.is_running():
            subprocess.run(['tmux', 'send-keys', '-t', self.tmux_session_name, 'C-c'])
            subprocess.run(['tmux', 'kill-session', '-t', self.tmux_session_name])
            await ctx.send("Minecraft server stopped.")
            return "Minecraft server stopped."
        else:
            await ctx.send("Minecraft server is not running.")
            return "Minecraft server is not running."

    @commands.command()
    async def restart(self, ctx, *args):
        stop_message = await self.stop()
        await ctx.send(stop_message)
        start_message = self.start()
        await ctx.send(start_message)
        return f"{stop_message}\n{start_message}"

    @commands.command()
    async def output(self, ctx, *args):
        await self.toggle_output(ctx)

    async def _show_output(self, channel):
        while self.output_displaying and self.is_running():
            output = subprocess.run(
                ['tmux', 'capture-pane', '-t', self.tmux_session_name, '-p'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if output.stdout:
                await channel.send(f'```{output.stdout.strip()}```')
            await asyncio.sleep(1)

    async def toggle_output(self, channel):
        if self.output_displaying:
            self.output_displaying = False
            if self.output_task is not None:
                self.output_task.cancel()
                self.output_task = None
            await channel.send("Stopped displaying Minecraft server output.")
        else:
            if self.is_running():
                self.output_displaying = True
                self.output_task = asyncio.create_task(self._show_output(channel))
                await channel.send("Started displaying Minecraft server output.")
            else:
                await channel.send("Minecraft server is not running.")

async def setup(client):
    await client.add_cog(MinecraftServer(client))