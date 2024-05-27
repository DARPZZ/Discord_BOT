from share import *
import pytz
from datetime import datetime, timedelta
matches_for_the_day=[]
async def scrape_matches():
    url = "https://www.ufc.com/events"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()
    soup = BeautifulSoup(text, 'html.parser')
    
    matches = soup.find_all('li', class_='l-listing__item')
    

    edt_timezone = pytz.timezone('America/New_York')
    copenhagen_timezone = pytz.timezone('Europe/Copenhagen')
    
    for match in matches:
        head_line = match.find_all('h3', class_= 'c-card-event--result__headline')
        match_info = match.find_all('div', class_='c-card-event--result__date tz-change-data')
        fighters = head_line[0].text.strip()
        stripped_match_info = match_info[0].text.strip()
        split_match_info = stripped_match_info.split(" ")
        month = split_match_info[1]
        day = split_match_info[2]
        time = split_match_info[4]
        time_zone = split_match_info[5]
        mma_kamp_cest = month + " " + day + " " + time + " " + time_zone
        race_date_1 = mma_kamp_cest.replace("PM", "").replace("May", "Maj").replace("Oct","Okt")
        cest_time = datetime.strptime(race_date_1, "%b %d %I:%M %p")
        cest_time = edt_timezone.localize(cest_time)
        copenhagen_time = cest_time.astimezone(copenhagen_timezone)
        mma_kamp_copenhagen = copenhagen_time.strftime("%d %B     %I:%M")
        matches_for_the_day.append(f"**Date and time:**\t {mma_kamp_copenhagen}\n**Headline:**\t {fighters}\n{'-'*60}\n ")
        #print(f"**Date and time:**\t {mma_kamp_copenhagen}\n**Headline:**\t {fighters}\n{'-'*60}\n ")
        #print(f"**Date**\t {mma_kamp_copenhagen}\n**Headline:**\t {fighters}\n{'-'*60}\n ")
        
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

