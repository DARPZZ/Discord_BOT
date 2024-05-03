import requests
import datetime
import aiohttp
from share import *
from bs4 import BeautifulSoup
import locale
from discord.ext import tasks
load_dotenv() 
fodbold_URL = os.getenv("fodbold_URL")
matche = os.getenv("matches")
matches_for_the_day =[]

@tasks.loop(minutes=1)
async def scrape_matches():
    url = fodbold_URL
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()
    soup = BeautifulSoup(text, 'html.parser')
    locale.setlocale(locale.LC_TIME, "da_DK.UTF-8")
    mydate = datetime.datetime.now()
    formatted_date = mydate.strftime("%e. %b")
    format_dt = formatted_date.split(" ")
    spiltted_date = format_dt[1] + " " +  format_dt[2]

    matches = soup.find_all('li', class_=matche)
    for match in matches:
        teams = match.find('div', class_='teams').text.strip()
        split_teams = teams.split("  ")
        formattted_teams = split_teams[0] + "\t VS \t" + split_teams[1]
        time = match.find('div', class_='date-time-wrapper').text.strip()
        formatted_time = time.split(" ");
        matchtime = formatted_time[0] + " " + formatted_time[1]
        if(spiltted_date == matchtime):
            matches_for_the_day.append(f"- ** Teams:\t {formattted_teams}\t\t\t\tTime:\t{formatted_time[2]} ** \n")
            
    channel = client.get_channel(1234600317090529392)
    if matches_for_the_day:
        matches_message = "\n".join( matches_for_the_day)
        await channel.send("<@&1234890120029536297>")
        await channel.send("**Todays matches:**")
        await channel.send(matches_message)
        matches_for_the_day.clear()
    else:
        await channel.send("No matches for today.")
        

now = datetime.datetime.now()
print(now.hour)
if now.hour < 8:
    hours_until_8 = 8 - now.hour
else:
    hours_until_8 = 24 - now.hour + 8
minutes_until_8 = hours_until_8 * 60 - now.minute
seconds_until_8 = minutes_until_8 * 60 - now.second
scrape_matches.change_interval(hours=24, minutes=0, seconds=0)