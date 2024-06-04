
from share import *
from datetime import datetime, timedelta
import locale
from pytz import timezone
from discord.ext import tasks
matches_for_the_day =[]

async def scrape_matches(url, channel):
    url = url
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()
    soup = BeautifulSoup(text, 'html.parser')
    mydate_time = datetime.now(timezone('Europe/Copenhagen'))
    mydate = mydate_time.date()
    mydate_string = str(mydate)
    matches = soup.find_all('div', class_='table-cell match')
    for match in matches:
        match_rank = match.get('tier')
        date = match.get('date')
        tournament = match.get('tournamentname')
        teamnames = match.find_all('div', class_='team-name')
        string_date= str(date)
        score= match.find_all('div', class_='c-match-score score c-match-score--small')
        
        if  teamnames:
            # convert match til min tid zone
            match_time = datetime.strptime(string_date, "%Y-%m-%dT%H:%M:%S.%f+00:00")
            match_time = match_time.replace(tzinfo=timezone('UTC')).astimezone(timezone('Europe/Copenhagen'))
            
            if mydate_string == str(match_time.date()):
                if match_rank == 'b' or match_rank =='s':
                    strip_score=score[0].text.strip()
                    firstteam = teamnames[0].text.strip()
                    secondteam = teamnames[1].text.strip()
                    new_time_string = match_time.strftime("%H:%M")
                    matches_for_the_day.append(f"**teams:** {firstteam}  VS  {secondteam}\n**Time:**{new_time_string}\n**Score:** {strip_score}\n**Tournament**: {tournament}\n{'-'*60}\n")
                    #print(f"**teams:** {firstteam}  VS  {secondteam}\n**Time:**{new_time_string}\n**Score:** {strip_score}\n**Tournament**: {tournament}\n{'-'*60}\n")
    channel = client.get_channel(channel)
    await channel.purge(limit=5)
    if matches_for_the_day:
        
        await channel.send("**Todays matches:**")
        matches_message = "\n".join( matches_for_the_day)
        for part in split_message(matches_message.split("\n")):
            await channel.send(part)
        matches_for_the_day.clear()
        return True
    else:
        await channel.send("No matches for today.")
        return False
