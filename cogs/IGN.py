import discord
import sys
from discord.ext import commands
import json
from postgres.models.User import User
from postgres.db import session
import re

class IGNCog(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_role("Re1 Guildies")
    async def register(self, ctx, ign):
        user = User(ctx.author.id, ign)
        try:
            instance = session.query(User).filter_by(id=str(ctx.author.id))
            if instance.first():
                instance.update({'id':str(ctx.author.id), 'ign':ign})
            else:
                session.add(user)
        except Exception as e:
            session.rollback()
            await ctx.send(f"Could not register {ign}: {e}")
        else:
            session.commit()
            await ctx.send(f"Registered {ign}")

    @commands.command()
    @commands.has_role("Re1 Guildies")
    async def getign(self, ctx, userID):
        try:
            # userID = str(userID[2:-1])
            userID = re.sub("[^0-9]", "", userID)
            result = session.query(User).filter_by(id=userID).first()
            await ctx.send(result.ign)
        except Exception as e:
            await ctx.send(f"Could not find an IGN for this user: {e}")


def setup(client):
    client.add_cog(IGNCog(client))
    print("IGNCog Loaded")