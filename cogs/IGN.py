import discord
from discord.ext import commands
import json

IGN_PATH = "igns.json"

class IGNCog(commands.Cog):

    def __init__(self, client, igns):
        self.client = client
        self.igns = igns

    @commands.command()
    async def register(self, ctx, ign):
        self.igns[str(ctx.author.id)] = ign
        
        with open(IGN_PATH, 'w') as outfile:
            json.dump(self.igns, outfile)

    @commands.command()
    async def ign(self, ctx, userID):
        try:
            userID = userID[2:-1]
            await ctx.send(self.igns[userID])
        except:
            await ctx.send("Could not find an IGN for this user please ensure you tag the user. ie. @Larry#1234")


def setup(client):
    with open (IGN_PATH, mode='r') as jsonfile:
        igns = json.load(jsonfile)
    jsonfile.close()
    
    client.add_cog(IGNCog(client, igns))
    print("IGNCog Loaded")