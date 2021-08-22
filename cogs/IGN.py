import discord
import sys
from discord.ext import commands
import json
from postgres.models.User import User
from postgres.db import session

class IGNCog(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
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
    async def ign(self, ctx, userID):
        try:
            userID = userID[2:-1]
            result = session.query(User).filter_by(id=userID).first()
            await ctx.send(result.ign)
        except:
            await ctx.send("Could not find an IGN for this user please ensure you tag the user. ie. @Larry#1234")


def setup(client):
    client.add_cog(IGNCog(client))
    print("IGNCog Loaded")