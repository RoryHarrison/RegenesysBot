import discord
from discord.ext import commands

class ReadyCog(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(status=discord.Status.online, activity=discord.Game('( ͡° ͜ʖ ͡°)'))
        print('Bot is now running')

    # @commands.command()
    # async def thread(self, ctx):
    #     msg = await ctx.send(ctx.message.content[8:])
    #     await msg.start_thread(name=ctx.message.content[8:])
    #     await ctx.message.delete()

def setup(client):
    client.add_cog(ReadyCog(client))