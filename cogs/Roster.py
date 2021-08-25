import discord
from discord.ext import commands
import json
import csv
from cogs.config.cog_utils import *
from postgres.db import session
from postgres.models.Roster import Roster
import re

class RosterCog(commands.Cog):


    def __init__(self, client):
        self.client = client
        

    @commands.command(aliases=['r'])
    @commands.has_role("Re1 Guildies")
    async def add(self, ctx, hero=None, asc=None, si=None, fi="0", en="E0"):
        if ctx.channel.category_id not in CATEGORIES:
            return

        id = str(ctx.author.id)

        if None in (hero, asc, si, fi, en):
            await ctx.send("Invalid Format, example: +roster lucius A 30 9")
            return
        else:
            hero = hero.title()
            asc = asc.upper()

        roster = Roster(id, hero, asc, si, fi, en)

        if not await check_registration(ctx):
            return

        validation = validate_roster_args(get_heroes(), roster)
        if not validation == True:
            await ctx.send(validation)
            return

        try:
            instance = session.query(Roster).filter_by(
            user = roster.user,
            hero = roster.hero
            ).first()
            if instance:
                instance.asc = roster.asc
                instance.si = roster.si
                instance.fi = roster.fi
                instance.en = roster.en
                session.commit()
            else:
                session.add(roster)
        except Exception as e:
            session.rollback()
            await ctx.send(f"Could not add that hero (DB Error): {e}")
            raise
        else:
            session.commit()
            await ctx.send(f"Added {roster.hero} for {ctx.author.name}")


    @commands.command(aliases=['cr'])
    @commands.has_role("Re1 Guildies")
    async def check(self, ctx, userID=None):
        if ctx.channel.category_id not in CATEGORIES:
            return

        if not await check_registration(ctx):
            return

        try:
            userID = re.sub("[^0-9]", "", userID)
            result = session.query(Roster).filter_by(user=userID).all()
            chunks = chunker(50, result)
        except:
            await ctx.send("Could not find user")
            return
        
        for chunk in chunks:
            roster_str = format_roster('Hero', 'Asc', 'SI', 'F', 'EN')
            for row in chunk:
                roster_str += format_roster(row.hero, row.asc, row.si, row.fi, row.en, newline=True)
            await ctx.send(f"```{roster_str}```")
            

def setup(client):
    client.add_cog(RosterCog(client))
    print("RosterCog Loaded")