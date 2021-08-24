import discord
from discord.ext import commands
import json
import csv
from cogs.config.cog_utils import *
from postgres.db import session
from postgres.models.Roster import Roster

ROSTER_PATH = "rosters.json"

class AdminRosterCog(commands.Cog):

    def __init__(self, client):
            self.client = client

    @commands.command(aliases=['del', 'delete'])
    @commands.has_role("Guild Leadership")
    async def d(self, ctx, userID=None):
        if ctx.channel.category_id not in CATEGORIES:
            return

        if not await check_registration(ctx):
            return

        try:
            userID = userID[2:-1]
            result = session.query(Roster).filter_by(user=userID).all()
            for row in result:
                print(row)
                session.delete(row)
            session.commit()
            await ctx.send("Deleted Roster")
        except Exception as e:
            await ctx.send(f"Could not find roster")


def setup(client):
    client.add_cog(AdminRosterCog(client))
    print("AdminRosterCog Loaded")