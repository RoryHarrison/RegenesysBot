import discord
from discord.ext import commands
from cogs.config.cog_utils import *
from postgres.db import session
from postgres.models.Wishlist import AEWish
from postgres.models.Roster import Roster

class WishlistCog(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_role("Re1 Guildies")
    async def compare(self, ctx):
        if ctx.channel.category_id not in CATEGORIES:
            return

        if not await check_registration(ctx):
            return

        wl_string = ""
        try:
            user_roster = session.query(Roster).filter_by(user=str(ctx.author.id)).all()
            wishlist = session.query(AEWish).all()
            chunks = chunker(30, wishlist)
        except:
            await ctx.send("Could not find your roster")
            return

        for chunk in chunks:
            for wl_item in chunk:
                wl_string += f" {format_roster(wl_item.hero, wl_item.asc, wl_item.si, wl_item.fi, wl_item.en)}"
                for row in user_roster:
                    if wl_item.hero == row.hero:
                        wl_string += f"\n[{format_roster(row.hero, row.asc, row.si, row.fi, row.en)}]\n"
            await ctx.send(f"```css\n{wl_string}```")

    @commands.command(aliases=['wishlistadd'])
    @commands.has_role("Guild Leadership")
    async def wla(self, ctx, hero=None, asc=None, si=None, fi=None, en="E0"):
        if ctx.channel.category_id not in CATEGORIES:
            return
        
        if None in (hero, asc, si, fi, en):
            await ctx.send("Invalid Format, example: +wla lucius A 30 9")
            return
        else:
            hero = hero.title()
            asc = asc.upper()

        aewish = AEWish(hero, asc, si, fi, en)

        validation = validate_roster_args(get_heroes(), aewish)
        if not validation == True:
            await ctx.send(validation)
            return

        try:
            instance = session.query(AEWish).filter_by(
            hero = aewish.hero
            ).first()
            if instance:
                instance.asc = aewish.asc
                instance.si = aewish.si
                instance.fi = aewish.fi
                instance.en = aewish.en
                session.commit()
            else:
                session.add(aewish)
        except Exception as e:
            session.rollback()
            await ctx.send(f"Could not add that hero (DB Error): {e}")
            raise
        else:
            session.commit()
            await ctx.send(f"{ctx.author.name} added {aewish.hero} to the AE Wishlist")

    @commands.command(aliases=['wishlistdel'])
    @commands.has_role("Guild Leadership")
    async def wld(self, ctx, hero):
        hero = hero.title()
        try:
            result = session.query(AEWish).filter_by(hero=hero).first()
            session.delete(result)
            session.commit()
            await ctx.send(f"{ctx.author.name} removed {hero} from the AE Wishlist")
        except Exception as e:
            await ctx.send(f"Could not find hero in wishlist")

    @commands.command(aliases=['wishlist'])
    @commands.has_role("Re1 Guildies")
    async def wl(self, ctx):
        result = session.query(AEWish).all()
        roster_str = format_roster('Hero', 'Asc', 'SI', 'F', 'EN')
        for row in result:
            roster_str += format_roster(row.hero, row.asc, row.si, row.fi, row.en, newline=True)
        await ctx.send(f"```{roster_str}```")

def setup(client):

    client.add_cog(WishlistCog(client))
    print("WishlistCog Loaded")