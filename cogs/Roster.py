import discord
from discord.ext import commands
import json
import csv

HERO_OFFSET = 10
OFFSET = 5
IGN_PATH = "igns.json"

ROSTER_PATH = "rosters.json"
HEROES_PATH = "heroes.csv"

class RosterCog(commands.Cog):


    def __init__(self, client, rosters):
        #Initialise roster dict
        self.rosters = rosters
        self.heroes = self.get_heroes(HEROES_PATH)
        self.client = client


    @commands.command()
    async def r(self, ctx, hero=None, asc=None, si=None, fi=None, en="E0"):
        id = str(ctx.author.id)
        hero = hero.title()
        asc = asc.upper()

        if not await self.check_registration(ctx):
            return

        validation = self.validate_roster_args(hero, asc, si, fi, en)
        if not validation == True:
            await ctx.send(validation)
            return

        if id in self.rosters:
            for idx, item in enumerate(self.rosters[id]):
                if item["Name"] == hero:
                    self.rosters[id][idx] = {"Name":hero, "Asc":asc, "SI":si, "F":fi, "En":en}
                    await ctx.send(f"Added {hero} for {ctx.author.name}")
                    return
                    
            self.rosters[id].append({"Name":hero, "Asc":asc, "SI":si, "F":fi, "En":en})
            
        else:
            self.rosters[id] = [{"Name":hero, "Asc":asc, "SI":si, "F":fi, "En":en}]
        
        self.write_rosters()
        await ctx.send(f"Added {hero} for {ctx.author.name}")
    

    @commands.command()
    async def cr(self, ctx, userID=None):
        
        if not await self.check_registration(ctx):
            return
        
        try:
            userID = userID[2:-1]
            user_roster = self.rosters[userID]
        except:
            await ctx.send("Could not find user")
            return
        
        roster_str = "Hero"; roster_str += ' ' * (HERO_OFFSET-4)
        roster_str += "Asc"; roster_str += ' ' * (OFFSET-3)
        roster_str += "SI"; roster_str += ' ' * (OFFSET-2)
        roster_str += "Furn"; roster_str += ' ' * (OFFSET-4)
        roster_str += "EN"
        
        for hero in user_roster:
            roster_str += f"\n{hero['Name']}"; roster_str += ' ' * (HERO_OFFSET-len(hero['Name']))
            roster_str += f"{hero['Asc']}"; roster_str += ' ' * (OFFSET-len(hero['Asc']))
            roster_str += f"{hero['SI']}"; roster_str += ' ' * (OFFSET-len(hero['SI']))
            roster_str += f"{hero['F']}"; roster_str += ' ' * (OFFSET-len(hero['F']))
            roster_str += f"{hero['En']}"
        
        await ctx.send(f"```{roster_str}```")


    @commands.command()
    async def d(self, ctx, userID=None):

        if not await self.check_registration(ctx):
            return

        try:
            userID = userID[2:-1]
            self.rosters.pop(userID)
        except:
            await ctx.send("Could not find user")

        self.write_rosters()


    def validate_roster_args(self, hero, asc, si, fi, en):
        if None in (hero, asc, si, fi, en):
            return "Invalid Format, example: +roster lucius A 30 9"
        if not hero in self.heroes:
            return "Not a valid hero"
        if not asc in ['E', 'E+', 'L', 'L+', 'M', 'M+', 'A', 'A1', 'A2', 'A3', 'A4', 'A5']:
            return "Please provide a valid Ascension level e.g. E+, A3 etc..."
        try:
            si = int(si)
            fi = int(fi)
        except:
            return "Please enter a valid SI and Furniture number"
        if not si in range(0, 41):
            return "Please enter an SI between 0 and 40"
        if not fi in range(0, 37):
            return "Please enter furniture between 0 and 36"
        if not en in ['E0', 'E30', 'E60', 'E80', 'E100']:
            return "Please enter a valid engravings value e.g. E30, E60"
        return True


    def get_heroes(self, path):
        hero_list = []
        with open(path, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                for item in row:
                    hero_list.append(item)
        return hero_list


    def write_rosters(self):
        with open(ROSTER_PATH, 'w') as jsonfile:
            json.dump(self.rosters, jsonfile)


    async def check_registration(self, ctx):
        id = ctx.author.id
        with open (IGN_PATH, mode='r') as jsonfile:
            igns = json.load(jsonfile)
        jsonfile.close()

        if str(id) in igns:
                return True
        else:
            await ctx.send("Please register your ign first")
            return False

            

def setup(client):
    with open(ROSTER_PATH, 'r') as jsonfile:
        rosters = json.load(jsonfile)

    client.add_cog(RosterCog(client, rosters))
    print("RosterCog Loaded")