from share import *
from discord.ext import tasks
import Football
import counter_valorant
import ufc
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
    has_matches = await counter_valorant.scrape_matches("https://bo3.gg/matches/current",1235813854580179125)
    if not has_matches:
        start_counterstrike_loop.change_interval(hours=3)
    else:
        start_counterstrike_loop.change_interval(hours=1)
@tasks.loop(hours=24)
async def start_valorant_loop():
   await counter_valorant.scrape_matches("https://bo3.gg/valorant/matches/current",1247488307768721439)

@tasks.loop(hours=144)
async def start_f1_loop():
    await F1.scrape_matches()


@tasks.loop(hours=144)
async def start_Ufc_loop():
    await ufc.scrape_matches()
