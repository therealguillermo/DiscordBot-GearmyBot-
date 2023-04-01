import discord
from discord.ext import commands
import yt_dlp
from musicPlayerModules.queue import Queue
import asyncio


FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
YDL_OPTIONS = {'format': 'bestaudio'}
ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'quiet': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    }
#greetingSource = discord.FFmpegPCMAudio("whatGoingOnMate.mp3")
#deliSource = discord.FFmpegPCMAudio("cartelyelling.mp4")
#fartedSource = discord.FFmpegPCMAudio("frtedSource.mp4")


class musicPlayer(commands.Cog):
    def __init__(self, Client):
        self.client = Client
        self.queue = Queue()
        self.voice_client = None
        self.sources = {}
        self.titles = {}
        print("Starting Up musicPlayer")

    async def mainLoop(self, ctx):
        print("mainloop started")
        while self.voice_client != None:
            queueNotEmpty = not self.queue.isEmpty()
            if queueNotEmpty:
                targetSource = self.queue.getFront()
                sourceExists = targetSource in self.sources.keys()

                if not self.voice_client.is_playing() and sourceExists:
                    self.voice_client.stop()
                    print(self.sources[targetSource])
                    self.voice_client.play(self.sources[targetSource], after=self.finishedPlaying)
                    print("finished")
                elif not sourceExists and queueNotEmpty:
                    try:
                        self.sources[targetSource] = await self.getSource(targetSource)
                    except:
                        await ctx.send(f"invalid link : {targetSource}")
                        self.queue.remove(targetSource)
            
            await asyncio.sleep(2)
        print("mainloop closed")
            # print(f"{self.voice_client.is_playing()}")
            # print(f"{self.queue}")
            # print(f"\n")

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("You're not in a voice channel")
        if ctx.voice_client is None:
            vc = ctx.author.voice.channel
            print(f"joining {vc}")
            try:
                await vc.connect()
            except Exception as e:
                print(e)
        elif self.voice_client == ctx.voice_client:
            await ctx.send("I'm already connected to this channel")
        else:
            await ctx.voice_client.move_to(ctx.author.voice.channel)
        self.voice_client = ctx.voice_client
        greetingSource = discord.FFmpegPCMAudio("whatGoingOnMate.mp3")
        try:
            print(ctx.voice_client.is_connected())
            ctx.voice_client.play(greetingSource, after=None)
        except Exception as e:
            print(str(e))
        await self.mainLoop(ctx)

    @commands.command()
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()
        self.queue.empty()
        self.voice_client = None

    @commands.command()
    async def play(self, ctx, url):
        if self.voice_client == None:
            await ctx.send("Why would you ask me to play something when i'm not in a voice channel dumbass")
            return
        self.queue.add(url)
        if not self.queue.isEmpty():
            self.voice_client.stop()

    @commands.command()
    async def next(self, ctx):
        if self.queue.getNext() == None:
            await ctx.send("Nothing next in queue")
            return
        else:
            self.voice_client.stop()

    @commands.command()
    async def addq(self, ctx, url):
        if self.voice_client == None:
            await ctx.send("Why would you ask me to add something when i'm not in a voice channel dumbass")
            return
        self.queue.add(url)
        if url not in self.sources.keys():
            self.sources[url] = await self.getSource(url)
        print(f"{url} added to q")

    @commands.command()
    async def Q(self, ctx):
        await ctx.send(f"{self.queue}\n{self.sources}")
        print(f"{self.queue}\n{self.sources}")

    @commands.command()
    async def harmonicaClip(self, ctx):
        if self.voice_client == None:
            await ctx.send("Why would you ask me to play something when i'm not in a voice channel dumbass")
            return
        self.voice_client.stop()
        deliSource = discord.FFmpegPCMAudio("cartelyelling.mp4")
        self.voice_client.play(deliSource, after=None)

    @commands.command()
    async def deliClip(self, ctx):
        if self.voice_client == None:
            await ctx.send("Why would you ask me to play something when i'm not in a voice channel dumbass")
            return
        self.voice_client.stop()
        fartedSource = discord.FFmpegPCMAudio("frtedSource.mp4")
        self.voice_client.play(fartedSource, after=None)

    @commands.command()
    async def queue(self, ctx):
        if len(self.queue) == 0:
            await ctx.send("Queue is currently empty")
            return
        str_queue = ""
        for i in range(len(self.queue)):
            pos = "Playing: " if i == 0 else str(i+1) + ")"
            add_str = f"{pos} {self.titles[self.queue.get(i)]}\n"
            str_queue += add_str
        await ctx.send(str_queue)

    async def getSource(self, url): 
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            print("downloaded")
            info = ydl.sanitize_info(info)
            print("sanitized")
            #url2 = info['formats'][0]['url']
            url2 = info['url']
            title = info['title']
            self.titles[url] = title
            videolen = info['duration']
            print(f"length : {videolen}\n", f"url : {url2}")
            #source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
            source = discord.FFmpegPCMAudio(url2, **FFMPEG_OPTIONS)
        return source

    def finishedPlaying(self, ctx):
        if ctx is None:
            self.sources.pop(self.queue.popFront())
        print(f"finished Playing {ctx}")

            
async def setup(client):
    await client.add_cog(musicPlayer(client))
