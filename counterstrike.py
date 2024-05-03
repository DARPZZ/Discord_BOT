import requests
import datetime
import aiohttp
from share import *
from bs4 import BeautifulSoup
import locale
from discord.ext import tasks
matches_for_the_day =[]

@tasks.loop(minutes=1)
async def scrape_matches_cs():
    url = "https://bo3.gg/matches/current"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()
    soup = BeautifulSoup(text, 'html.parser')
    mydate_time = datetime.datetime.now()
    mydate = mydate_time.date()
    mydate_string = str(mydate)
    matches = soup.find_all('div', class_='table-cell match')
    for match in matches:
        match_rank = match.get('tier')
        date = match.get('date')
        teamnames = match.find_all('div', class_='team-name')
        string_date= str(date)
        date_string = string_date[0:10]
        time_string = string_date[11:16]
        if  teamnames:
            if mydate_string == date_string:
                if match_rank == 'b' or match_rank =='s':
                    firstteam = teamnames[0].text.strip()
                    secondteam = teamnames[1].text.strip()
                    #print(f"Team : {firstteam}   VS    Team : {secondteam}        time: {time_string} ")
                    matches_for_the_day.append(f"** - Team : {firstteam}   VS    Team : {secondteam}        time: {time_string} **  \n")
    channel = client.get_channel(1235813854580179125)
    await channel.send("<@&1235818483640434798>")
    await channel.send("**Todays matches:**")
    matches_message = "\n".join( matches_for_the_day)
    await channel.send(matches_message)

            
