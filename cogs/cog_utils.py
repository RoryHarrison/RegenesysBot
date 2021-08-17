import csv
import json

HERO_OFFSET = 10
OFFSET = 5

IGN_PATH = "igns.json"
ROSTER_PATH="rosters.json"
HEROES_PATH = "heroes.csv"
WL_PATH = "wishlist.json"

def get_heroes():
    hero_list = []
    with open(HEROES_PATH, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            for item in row:
                hero_list.append(item)
    return hero_list

def write_json(items, path):
    with open(path, 'w') as jsonfile:
        json.dump(items, jsonfile)

def validate_roster_args(heroes, hero, asc, si, fi, en):
    if None in (hero, asc, si, fi, en):
        return "Invalid Format, example: +roster lucius A 30 9"
    if not hero in heroes:
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

async def check_registration(ctx):
    id = ctx.author.id
    with open (IGN_PATH, mode='r') as jsonfile:
        igns = json.load(jsonfile)
    jsonfile.close()

    if str(id) in igns:
            return True
    else:
        await ctx.send("Please register your ign first")
        return False

def format_roster(name, asc, si, f, en, newline=False):

    if newline == True:
        roster_str = f"\n{name}"
    else:
        roster_str = f"{name}"
    
    roster_str += ' ' * (HERO_OFFSET-len(name))
    roster_str += f"{asc}"; roster_str += ' ' * (OFFSET-len(asc))
    roster_str += f"{si}"; roster_str += ' ' * (OFFSET-len(si))
    roster_str += f"{f}"; roster_str += ' ' * (OFFSET-len(f))
    roster_str += f"{en}"

    return roster_str