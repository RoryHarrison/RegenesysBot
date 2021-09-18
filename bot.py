import discord
from discord.ext import commands
import os

discord_token = os.environ['DISCORD_TOKEN']

client = commands.Bot(command_prefix="+")

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

for cog in ['Roster', 'AdminRoster', 'Wishlist',  'IGN', 'Ready', 'Rand']:
    client.load_extension(f'cogs.{cog}')

client.run(discord_token)
# client.run('ODc5Nzg3NzYyMTAwODg3NjIz.YSU0NA.22vvAHTKLIpqz3-EPlGyKxNNCDY')