from share import *
from discord.ext import tasks
import Football
import counterstrike
@tasks.loop(hours=1) 
async def start_football_loop():
    await Football.scrape_matches()

@tasks.loop(hours=1)  
async def start_counterstrike_loop():
    await counterstrike.scrape_matches()