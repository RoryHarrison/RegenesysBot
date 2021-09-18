import discord
from discord.ext import commands
from cogs.config.cog_utils import *
from postgres.db import session
from postgres.models.Roster import Roster
import random

class RosterCog(commands.Cog):


    def __init__(self, client):
        self.client = client
        

    @commands.command(aliases=['random'])
    @commands.has_role("Re1 Guildies")
    async def rand(self, ctx, hero=None, asc=None, si=None, fi="0", en="E0"):
        try:
            heroes = get_heroes()
            await ctx.send(f"{ctx.author.name}'s Hero: {random.choice(heroes).hero}")
        except Exception as e:
            await ctx.send(f"Error: {e}")


def setup(client):
    client.add_cog(RosterCog(client))
    print("RandCog Loaded")