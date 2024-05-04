import datetime
import aiohttp
from share import *
from discord.ext import tasks
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
    ongoing_time = mydate.strftime("%H:%M")
    matches = soup.find_all('li', class_=matche)
    for match in matches:
        teams = match.find('div', class_='teams').text.strip()
        split_teams = teams.split("  ")
        formattted_teams = split_teams[0] + "\t VS \t" + split_teams[1]
        time = match.find('div', class_='date-time-wrapper').text.strip()
        formatted_time = time.split(" ");
        matchtime = formatted_time[0] + " " + formatted_time[1]
        if(spiltted_date == matchtime):
            if ongoing_time > formatted_time[2]:
                matches_for_the_day.append(f"- ** Teams:\t {formattted_teams}\t\t\t\tTime:\t{formatted_time[2]} \t\t Status: Ongoing ** \n")
            elif ongoing_time < formatted_time[2]:
                matches_for_the_day.append(f"- ** Teams:\t {formattted_teams}\t\t\t\tTime:\t{formatted_time[2]} \t\t Status: Upcomming ** \n")
            
    channel = client.get_channel(1234600317090529392)
    await channel.purge(limit=5)
    if matches_for_the_day:
        matches_message = "\n".join( matches_for_the_day)
        await channel.send("<@&1234890120029536297>")
        await channel.send("**Todays matches:**")
        for part in split_message(matches_message.split("\n")):
            await channel.send(part)
        matches_for_the_day.clear()
    else:
        await channel.send("No matches for today.")