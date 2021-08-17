import discord
from discord.ext import commands

import sys, os
sys.path.append('C:/Users/roryh/Projects/')

client = commands.Bot(command_prefix="+")

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

for cog in ['Roster', 'AdminRoster', 'Wishlist',  'IGN', 'Ready']:
    client.load_extension(f'cogs.{cog}')

client.run('ODA2NTA2NjA0NzQwMDgzNzMy.YBqbzg._5DyJZxjT6YzLwOQaeyfTtqRj6s')