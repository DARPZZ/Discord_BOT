from share import *
from discord.ext import tasks
import Football
import counterstrike
import Ufc
import F1
@tasks.loop(hours=1) 
async def start_football_loop():
    has_matches = await Football.scrape_matches()
    if not has_matches:
        start_football_loop.change_interval(hours=3)
    else:
        start_football_loop.change_interval(hours=1)

@tasks.loop(hours=1)
async def start_counterstrike_loop():
    has_matches = await counterstrike.scrape_matches()
    if not has_matches:
        start_counterstrike_loop.change_interval(hours=3)
    else:
        start_counterstrike_loop.change_interval(hours=1)

@tasks.loop(hours=144)
async def start_f1_loop():
    await F1.scrape_matches()


@tasks.loop(hours=144)
async def start_Ufc_loop():
    await Ufc.scrape_matches()
