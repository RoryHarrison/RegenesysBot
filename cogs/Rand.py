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
        if ctx.channel.id == 888604446416842802 or ctx.channel.category_id in [824341262168621057, 879772050993057813]:
            pass
        else:
            return

        try:
            heroes = get_heroes()
            hero = "Oops"
            while True:
                x = random.choice(heroes)
                if(x.faction not in ["Celestial", "Hypogean", "Dimensional"]):
                    hero = x.hero
                    break
                
            await ctx.send(f"{ctx.author.name}'s Hero: {hero}")
        except Exception as e:
            await ctx.send(f"Error: {e}")


def setup(client):
    client.add_cog(RosterCog(client))
    print("RandCog Loaded")