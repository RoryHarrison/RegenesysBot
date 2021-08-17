import discord
from discord.ext import commands
import json
import csv
from cogs.cog_utils import *

ROSTER_PATH = "rosters.json"

class AdminRosterCog(commands.Cog):

    def __init__(self, client, rosters, wishlist):
            self.rosters = rosters
            self.heroes = get_heroes()
            self.wishlist = wishlist
            self.client = client


def setup(client):
    with open(ROSTER_PATH, 'r') as jsonfile:
        rosters = json.load(jsonfile)
    with open(WL_PATH, 'r') as jsonfile:
        wishlist = json.load(jsonfile)

    client.add_cog(AdminRosterCog(client, rosters, wishlist))
    print("AdminRosterCog Loaded")