import re
import requests
from datetime import datetime, timedelta
import pytz 
from share import *
matches_for_the_day =[]


async def scrape_matches():
    url = "https://bo3.gg/matches/current"
    headers = {
        'accept-language': 'da-DK,da;q=0.9,en-US;q=0.8,en;q=0.7',
      
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            text = await response.text()
    soup = BeautifulSoup(text, 'html.parser')
    mydate_time = datetime.now()
    mydate = mydate_time.date()
    mydate = mydate.strftime("%d-%m")
    mydate_string = str(mydate)
    locale.setlocale(locale.LC_TIME, "da_DK.UTF-8")
    matches = soup.find_all('div', class_= 'c-matches-group-rows')
    for match in matches:
        tableRows = match.find_all('div', class_='table-row table-row--upcoming')
        for tableRow in tableRows:
            ADate = tableRow.find('a', class_='c-global-match-link table-cell')
            if ADate:
                href = ADate.get('href') 
                date_match = re.search(r'\d{2}-\d{2}-\d{4}', href)
                match_date = date_match.group(0)
                match_date = match_date.split('-')
                match_date =  match_date[0] + '-' + match_date[1]
                if (match_date == mydate_string):
                    matchTime = tableRow.find('span', class_='time').text.strip()
                    teamnames = tableRow.find_all('div', class_='team-name')
                    firstteam = teamnames[0].text.strip()
                    secondteam = teamnames[1].text.strip()
                    time_object = datetime.strptime(matchTime, "%H:%M")
                    time_object += timedelta(hours=2)
                    new_time_string = time_object.strftime("%H:%M")
                    #print(f"**Teams: ** {firstteam} VS {secondteam}\n**Time: ** {new_time_string}\n{'-'*60}\n")
                    matches_for_the_day.append(f"**Teams: ** {firstteam} VS {secondteam}\n**Time: ** {new_time_string}\n{'-'*60}\n")
        
    channel = client.get_channel(1235813854580179125)
    await channel.purge(limit=25)
    if matches_for_the_day:
        matches_message = "\n".join( matches_for_the_day)
        matches_for_the_day.clear()
        await channel.send("<@&1235818483640434798>")
        await channel.send("**Todays matches:**")
        for part in split_message(matches_message.split("\n")):
            await channel.send(part)
    else:
        await channel.send("No matches for today.")
