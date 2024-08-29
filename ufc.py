import aiohttp
import asyncio
from bs4 import BeautifulSoup
import pytz
from datetime import datetime
import locale
from share import *
matches_for_the_day = []

async def scrape_matches():
    url = "https://www.ufc.com/events"
    headers = {"Accept-Language": "da-DK,da;q=0.9,en-US;q=0.8,en;q=0.7"}
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            text = await response.text()
           
    soup = BeautifulSoup(text, 'html.parser')
    locale.setlocale(locale.LC_TIME, "da_DK.UTF-8") 
    matches = soup.find_all('div', class_='l-listing__item views-row')
    
    edt_timezone = pytz.timezone('America/New_York')
    copenhagen_timezone = pytz.timezone('Europe/Copenhagen')
    
    french_to_danish_month = {
        'janvier': 'januar',
        'février': 'februar',
        'mar': 'marts',
        'avr': 'april',
        'mai': 'maj',
        'juin': 'juni',
        'juil': 'juli',
        'aoû': 'august',
        'septembre': 'september',
        'octobre': 'oktober',
        'novembre': 'november',
        'décembre': 'december'
    }
    
    for match in matches:
        head_line = match.find_all('h3', class_='c-card-event--result__headline')
        match_info = match.find_all('div', class_='c-card-event--result__date tz-change-data')
        fighters = head_line[0].text.strip()
        stripped_match_info = match_info[0].text.strip()
        split_match_info = stripped_match_info.split(" ")
        french_month = split_match_info[1]
        danish_month = french_to_danish_month.get(french_month.lower(), french_month)
        day = split_match_info[2]
        time_str = split_match_info[3] + " " + split_match_info[4]
        
        if '/' in time_str:
            time_str = time_str.replace('/', '').strip()
            time_format = "%B %d %H:%M"
        else:
            time_format = "%B %d %I:%M %p"

        mma_kamp_cest = f"{danish_month} {day} {time_str}"

        try:
            cest_time = datetime.strptime(mma_kamp_cest, time_format)
        except ValueError as e:
            print(f"Error parsing date and time: {e}")
            continue
        
        cest_time = edt_timezone.localize(cest_time)
        copenhagen_time = cest_time.astimezone(copenhagen_timezone)
        mma_kamp_copenhagen = copenhagen_time.strftime("%d %B %I:%M %p")
        #print(f"**Date and time:**\t {mma_kamp_copenhagen}\n**Headline:**\t {fighters}\n{'-'*60}\n ")
        matches_for_the_day.append(f"**Date and time:**\t {mma_kamp_copenhagen}\n**Headline:**\t {fighters}\n{'-'*60}\n ")
        
    channel = client.get_channel(1234600336291790980)
    await channel.purge(limit=5)
    if matches_for_the_day:
        await channel.send("<@&1234891079699009651>")
        await channel.send("**Todays matches:**")
        matches_message = "\n".join( matches_for_the_day)
        for part in split_message(matches_message.split("\n")):
            await channel.send(part)
        matches_for_the_day.clear()
    else:
        await channel.send("No matches for today.")
 

