import aiohttp
import asyncio
from bs4 import BeautifulSoup
import pytz
from datetime import datetime
from share import *
matches_for_the_day = []

async def scrape_matches():
    matches_for_the_day.clear()
    url = "https://www.ufc.com/events"
    
    headers = {
        'accept-language': 'da-DK,da;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        'cookie': 'STYXKEY_region=WORLD.DK.en-zxx.Default'
    }
    
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            text = await response.text()
           
    soup = BeautifulSoup(text, 'html.parser')
    matches = soup.find_all('div', class_='l-listing__item views-row')
    
    for match in matches:
        head_line = match.find_all('h3', class_='c-card-event--result__headline')
        match_info = match.find_all('div', class_='c-card-event--result__date tz-change-data')
        fighters = head_line[0].text.strip()
        stripped_match_info = match_info[0].text.strip()
        split_match_info = stripped_match_info.split(" ")
        month = split_match_info[1].capitalize()
        day = split_match_info[2].strip(',')
        time = split_match_info[4]
        time_zone = split_match_info[5]
        time += time_zone
        mma_kamp_edt = f" {month} {day} {time}"
        matches_for_the_day.append(f"**Date and time:** {mma_kamp_edt} CEST\n**Headline:** {fighters}\n{'-'*60}\n ")
            


    channel = client.get_channel(1278765738345365504)
    await channel.purge(limit=5)
    if matches_for_the_day:
        matches_message = "\n".join( matches_for_the_day)
        await channel.send("<@&1234890120029536297>")
        await channel.send("**Todays matches:**")
        for part in split_message(matches_message.split("\n")):
            await channel.send(part)

    else:
        await channel.send("No matches for today.")



