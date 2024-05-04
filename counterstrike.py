
from share import *
from datetime import datetime, timedelta
import locale

from discord.ext import tasks
matches_for_the_day =[]

async def scrape_matches():
    url = "https://bo3.gg/matches/current"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()
    soup = BeautifulSoup(text, 'html.parser')
    mydate_time = datetime.now()
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
                    time_object = datetime.strptime(time_string, "%H:%M")
                    time_object += timedelta(hours=2)
                    new_time_string = time_object.strftime("%H:%M")
                    matches_for_the_day.append(f"** - Team : {firstteam}   VS    Team : {secondteam}        time: {new_time_string} **  \n")
    channel = client.get_channel(1235813854580179125)
    await channel.purge(limit=5)
    await channel.send("<@&1235818483640434798>")
    await channel.send("**Todays matches:**")
    matches_message = "\n".join( matches_for_the_day)
    matches_for_the_day.clear()
    await channel.send(matches_message)