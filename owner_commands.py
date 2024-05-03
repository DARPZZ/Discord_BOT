from share import *
from Football import scrape_matches
from counterstrike import scrape_matches_cs
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('!football'):
        await print("ffff")
        await scrape_matches()
    elif message.content.startswith('!CS'):
        print("hest")
        await scrape_matches_cs()
        
        