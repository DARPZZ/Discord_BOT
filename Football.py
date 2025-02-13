import datetime
import aiohttp
from share import *
from discord.ext import tasks
matches_for_the_day =[]



async def scrape_matches():
    loop_bool = True
    url = "https://www.livescore.dk/fodbold-i-tv/"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()
    soup = BeautifulSoup(text, 'html.parser')
    todays_matches = soup.find('div', class_='tv-table tv-table--football')
    football_match = todays_matches.find_next()
    while loop_bool:
        match = football_match.find_next_sibling()
        football_match = match
        if match.find('div', class_='date'):
            loop_bool = False
            break
        teams = football_match.find('span', class_='text').text.strip()
        tid = football_match.find('div', class_='time').text.strip()
        kanal = football_match.find('div', class_='chanels')
        img_tag = kanal.find('img')
        kanal = img_tag.get('alt', 'No alt attribute') if img_tag else 'No image found'
        league = football_match.find('div', class_='league')
        real_league = league.find('span', class_='text').text.strip()
        matches_for_the_day.append(f"**Teams:** {teams} \n**Tid:** {tid}\n**Liga:** {real_league} \n**Kanal:** {kanal} \n{'-'*60}\n ")
    channel = client.get_channel(1234600317090529392)
    await channel.purge(limit=25)
    if matches_for_the_day:
        matches_message = "\n".join(matches_for_the_day)
        matches_for_the_day.clear()
        await channel.send("<@&1234866967630839870>")
        await channel.send("**Today's matches:**")
        for part in split_message(matches_message.split("\n")):
            await channel.send(part)
    else:
        await channel.send("No matches for today.")
            