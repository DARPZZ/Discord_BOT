from share import *
from discord.ext import tasks
import Football
import counterstrike
@tasks.loop(minutes=5)
async def start_loop():
    await Football.scrape_matches()
    await counterstrike.scrape_matches()
    