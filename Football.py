import datetime
import aiohttp
from share import *
from discord.ext import tasks
load_dotenv() 
fodbold_URL = os.getenv("fodbold_URL")
matche = os.getenv("matches")
matches_for_the_day =[]



async def scrape_matches():
    i =1
    url = "https://www.livescore.dk/fodbold-i-tv/"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()
    soup = BeautifulSoup(text, 'html.parser')

    header = soup.find_all('div', class_='event')
    for match in header:
        time = match.find('div', class_='time').text.strip()
        teams = match.find('span', class_='text').text.strip()
        league = match.find('div', class_='league').text.strip()
        i += 1
        matches_for_the_day.append(f"**Teams:** {teams} \n**League:** {league}\n**Time:** {time}\n{'-'*60}\n ")
        if(i ==7):
           
            channel = client.get_channel(1234600317090529392)
            await channel.purge(limit=5)
            if matches_for_the_day:
                matches_message = "\n".join( matches_for_the_day)
                await channel.send("<@&1234890120029536297>")     
                await channel.send("**Todays matches:**")
                for part in split_message(matches_message.split("\n")):
                    await channel.send(part)
                matches_for_the_day.clear()
                return True
            else:
                await channel.send("No matches for today.")
                return False
            