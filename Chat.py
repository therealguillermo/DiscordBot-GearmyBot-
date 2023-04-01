import discord
from discord.ext import commands
import asyncio
import openai
from api_keys import APIKEY


class Chat(commands.Cog):
    def __init__(self, Client):
        self.client = Client
        self.messages = [
                    {"role": "system", "content": "You're name is the GearmyBot, You answer questions when asked and you try to be as acurate as possible"},
                ]
        openai.api_key = APIKEY.getKey('openai')
        print("Starting Up ChatBot")

    @commands.command()
    async def image(self, ctx, *args):
        size = "1024x1024"
        prompt = ' '.join(args)
        message = await ctx.send("Loading image please wait...")
        failed = False
        try:
            response = openai.Image.create(
            prompt=prompt,
            n=1,
            size=size
            )
        except Exception as e:
            print(str(e))
            failed = True
        await message.delete()
        if failed:
            await ctx.send("Image failed to generate cus you typed a bad word you drug addict")
            return
        image_url = response['data'][0]['url']
        await ctx.send(image_url)


    @commands.command()
    async def chat(self, ctx, *args):
        prompt = ' '.join(args)
        self.messages.append({"role": "user", "content": prompt})
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0301",
                messages=self.messages
            )
            response_text = response['choices'][0]['message']['content']
            self.messages.append({"role": "assistant", "content": response_text})
            await ctx.send(response_text)
        except Exception as e:
            print(str(e))
            await ctx.send(f'error {str(e)}')


async def setup(client):
    await client.add_cog(Chat(client))