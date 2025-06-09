from share import *
from discord.ext import tasks
import Football
import CounterStrike as CounterStrike
import ufc
import F1
import twitch
@tasks.loop(hours=1) 
async def start_football_loop():
    has_matches = await Football.scrape_matches()
    if not has_matches:
        start_football_loop.change_interval(hours=3)
    else:
        start_football_loop.change_interval(hours=1)
        
@tasks.loop(hours=1) 
async def twitch_loop():
    await twitch.get_live_twitch_streamer(['KmartPoker','shroud'])

@tasks.loop(hours=1)
async def start_counterstrike_loop():
    has_matches = await CounterStrike.scrape_matches()
    if not has_matches:
         start_counterstrike_loop.change_interval(hours=3)
    else:
         start_counterstrike_loop.change_interval(hours=1)
        
@tasks.loop(hours=48)
async def start_f1_loop():
    await F1.scrape_matches()
    
@tasks.loop(hours=48)
async def start_f1_driver_loop():
    await F1.scrape_driver_standing()
    
@tasks.loop(hours=48)
async def start_F1_Team_loop():
    await F1.scrape_team_standing()
    

@tasks.loop(hours=48)
async def start_Ufc_loop():
    await ufc.scrape_matches()
