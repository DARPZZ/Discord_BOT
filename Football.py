import requests
import datetime
import aiohttp
from share import *
from bs4 import BeautifulSoup
import locale
load_dotenv() 
fodbold_URL = os.getenv("fodbold_URL")
matche = os.getenv("matches")
matches_for_the_day =[]
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
        time = match.find('div', class_='date-time-wrapper').text.strip()
        formatted_time = time.split(" ");
        matchtime = formatted_time[0] + " " + formatted_time[1]
        if(spiltted_date == matchtime):
            matches_for_the_day.clear()
            matches_for_the_day.append(f"Teams:\t {teams}\t\t\t\t\t\t\tTime:\t{formatted_time[2]}")


            
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$matches'):
        await scrape_matches()  
        if matches_for_the_day:
            matches_message = "\n".join( matches_for_the_day)
            matches_message_format = "**" + matches_message + "**"
            await message.channel.send(matches_message_format)
        else:
            await message.channel.send("No matches for today.")
            


