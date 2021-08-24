import csv
import json
from postgres.db import session
from postgres.models.User import User
from postgres.models.Hero import Hero
import itertools

HERO_OFFSET = 10
OFFSET = 5
HEROES_PATH = "heroes.csv"
CATEGORIES = [879701970041057350, 824341262168621057, 879772050993057813]

def get_heroes():
    try:
        return session.query(Hero).all()
    except:
        print("get_heroes failed")
        raise

def validate_roster_args(heroes, roster):
    if None in (roster.hero, roster.asc, roster.si, roster.fi, roster.en):
        return "Invalid Format, example: +roster lucius A 30 9"
    names = [h.hero for h in heroes]
    if not roster.hero in names:
        return "Not a valid hero"
    if not roster.asc in ['E', 'E+', 'L', 'L+', 'M', 'M+', 'A', 'A1', 'A2', 'A3', 'A4', 'A5']:
        return "Please provide a valid Ascension level e.g. E+, A3 etc..."
    try:
        si = int(roster.si)
        fi = int(roster.fi)
    except:
        return "Please enter a valid SI and Furniture number"
    if not si in range(0, 41):
        return "Please enter an SI between 0 and 40"
    if not fi in range(0, 37):
        return "Please enter furniture between 0 and 36"
    if roster.asc not in ['A', 'A1', 'A2', 'A3', 'A4', 'A5'] and fi != 0:
        return "Cannot add furniture to an unascended hero"
    if not roster.en in ['E0', 'E30', 'E60', 'E80', 'E100']:
        return "Please enter a valid engravings value e.g. E30, E60"
    return True

async def check_registration(ctx):
    if session.query(User).filter_by(id=str(ctx.author.id)).first():
        return True
    else:
        await ctx.send("Please register your ign first")
        return False

def chunker(n, iterable):
    it = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(it, n))
        if not chunk:
            return
        yield chunk
    

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