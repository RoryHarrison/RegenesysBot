import discord
from discord.ext import commands
import json
import csv
from RegenesysBot.cogs.cog_utils import *

ROSTER_PATH = "rosters.json"

class AdminRosterCog(commands.Cog):

    def __init__(self, client, rosters, wishlist):
            self.rosters = rosters
            self.heroes = get_heroes()
            self.wishlist = wishlist
            self.client = client


    @commands.command(aliases=['wishlistadd'])
    @commands.has_role("Guild Leadership")
    async def wla(self, ctx, hero=None, asc=None, si=None, fi=None, en="E0"):
        if None in (hero, asc, si, fi, en):
            await ctx.send("Invalid Format, example: +wla lucius A 30 9")
            return
        else:
            hero = hero.title()
            asc = asc.upper()

        validation = validate_roster_args(self.heroes, hero, asc, si, fi, en)
        if not validation == True:
            await ctx.send(validation)
            return

        for idx, item in enumerate(self.wishlist):
            if item['Name'] == hero:
                self.wishlist[idx] = {"Name":hero, "Asc":asc, "SI":si, "F":fi, "En":en}
                write_json(self.wishlist, WL_PATH)
                await ctx.send(f"{ctx.author.name} added {hero} to Wishlist")
                return

        self.wishlist.append({"Name":hero, "Asc":asc, "SI":si, "F":fi, "En":en})
        write_json(self.wishlist, WL_PATH)
        await ctx.send(f"{ctx.author.name} added {hero} to Wishlist")

    @commands.command(aliases=['wishlistdel'])
    @commands.has_role("Guild Leadership")
    async def wld(self, ctx, hero):
        for idx, item in enumerate(self.wishlist):
            if item['Name'] == hero:
                del self.wishlist[idx]
                write_json(self.wishlist, WL_PATH)
                await ctx.send(f"{ctx.author.name} removed {hero} from Wishlist")
                return
        ctx.send("Could not find that hero in the wishlist")

    @commands.command(aliases=['wishlist'])
    async def wl(self, ctx):
        roster_str = format_roster('Hero', 'Asc', 'SI', 'F', 'EN') 
        for hero in self.wishlist:
            roster_str += format_roster(hero['Name'], hero['Asc'], hero['SI'], hero['F'], hero['En'], newline=True)
        await ctx.send(f"```{roster_str}```")


def setup(client):
    with open(ROSTER_PATH, 'r') as jsonfile:
        rosters = json.load(jsonfile)
    with open(WL_PATH, 'r') as jsonfile:
        wishlist = json.load(jsonfile)

    client.add_cog(AdminRosterCog(client, rosters, wishlist))
    print("AdminRosterCog Loaded")