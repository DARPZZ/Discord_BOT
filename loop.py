from share import *
from discord.ext import tasks
import Football
import counterstrike
@tasks.loop(hours=1)  # adjust the hours as per your requirement for Football
async def start_football_loop():
    await Football.scrape_matches()

@tasks.loop(hours=1)  # adjust the hours as per your requirement for Counterstrike
async def start_counterstrike_loop():
    await counterstrike.scrape_matches()