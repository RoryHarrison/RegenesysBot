import discord
from discord.ext import commands
import json
import csv
from RegenesysBot.cogs.cog_utils import *

class RosterCog(commands.Cog):


    def __init__(self, client, rosters, wishlist):
        self.wishlist = wishlist
        self.rosters = rosters
        self.heroes = get_heroes()
        self.client = client
        


    @commands.command(aliases=['roster'])
    async def r(self, ctx, hero=None, asc=None, si=None, fi=None, en="E0"):
        id = str(ctx.author.id)

        if None in (hero, asc, si, fi, en):
            await ctx.send("Invalid Format, example: +roster lucius A 30 9")
            return
        else:
            hero = hero.title()
            asc = asc.upper()

        if not await check_registration(ctx):
            return

        validation = validate_roster_args(self.heroes, hero, asc, si, fi, en)
        if not validation == True:
            await ctx.send(validation)
            return

        if id in self.rosters:
            for idx, item in enumerate(self.rosters[id]):
                if item["Name"] == hero:
                    self.rosters[id][idx] = {"Name":hero, "Asc":asc, "SI":si, "F":fi, "En":en}
                    write_json(self.rosters, ROSTER_PATH)
                    await ctx.send(f"Added {hero} for {ctx.author.name}")
                    return
                    
            self.rosters[id].append({"Name":hero, "Asc":asc, "SI":si, "F":fi, "En":en})
        else:
            self.rosters[id] = [{"Name":hero, "Asc":asc, "SI":si, "F":fi, "En":en}]
        
        write_json(self.rosters, ROSTER_PATH)
        await ctx.send(f"Added {hero} for {ctx.author.name}")
    

    @commands.command(aliases=['check', 'checkroster', 'cr'])
    async def c(self, ctx, userID=None):
        
        if not await check_registration(ctx):
            return
        
        try:
            userID = userID[2:-1]
            user_roster = self.rosters[userID]
        except:
            await ctx.send("Could not find user")
            return
        
        roster_str = format_roster('Hero', 'Asc', 'SI', 'F', 'EN') 
        for hero in user_roster:
            roster_str += format_roster(hero['Name'], hero['Asc'], hero['SI'], hero['F'], hero['En'], newline=True)
        
        await ctx.send(f"```{roster_str}```")

 
    @commands.command(aliases=['del', 'delete'])
    @commands.has_role("Guild Leadership")
    async def d(self, ctx, userID=None):

        if not await check_registration(ctx):
            return

        try:
            userID = userID[2:-1]
            self.rosters.pop(userID)
        except:
            await ctx.send("Could not find roster")

        write_json(self.rosters, ROSTER_PATH)

    @commands.command(aliases=['benchmark', 'bench', 'bm'])
    @commands.has_role("Guild Leadership")
    async def b(self, ctx):

        if not await check_registration(ctx):
            return

        wl_string = ""
        user_roster = self.rosters[str(ctx.author.id)]
        for wl_item in self.wishlist:
            wl_string += f" {format_roster(wl_item['Name'], wl_item['Asc'], wl_item['SI'], wl_item['F'], wl_item['En'])}"
            for hero in user_roster:
                if wl_item['Name'] == hero['Name']:
                    wl_string += f"\n[{format_roster(hero['Name'], hero['Asc'], hero['SI'], hero['F'], hero['En'])}]\n"
        await ctx.send(f"```css\n{wl_string}```")
            

def setup(client):
    with open(ROSTER_PATH, 'r') as jsonfile:
        rosters = json.load(jsonfile)
    with open(WL_PATH, 'r') as jsonfile:
        wishlist = json.load(jsonfile)

    client.add_cog(RosterCog(client, rosters, wishlist))
    print("RosterCog Loaded")