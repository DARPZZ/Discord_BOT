import requests
import datetime
import pytz 
from share import *
matches_for_the_day =[]

def split_message(lines, limit=2000):
    """Splits a list of lines into chunks each of size less than limit."""
    messages = []
    current_message = ""
    for line in lines:
        if len(current_message) + len(line) + 1 > limit: 
            messages.append(current_message)
            current_message = line
        else:
            current_message += "\n" + line
    messages.append(current_message) 
    return messages


async def scrape_matches():
    url = "https://www.skysports.com/f1/schedule-results"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()
    soup = BeautifulSoup(text, 'html.parser')
    locale.setlocale(locale.LC_TIME, "da_DK.UTF-8")
    races = soup.find_all('div', class_= 'f1-races__race-inner')
    mydate = datetime.datetime.now()
    formatted_date = mydate.strftime("%d %b").strip()
    for race in races:
        table_row = race.find_all('tr',class_='standing-table__row')
        r_date = race.find_all('p', class_='f1-races__race-date')

        new_date_for_race = r_date[0].text.strip()[0:2]
        new_month_for_race = r_date[0].text.strip()[5:8]
        race_date =str(mydate.year) + "-" + new_month_for_race + "-" + new_date_for_race
        race_date_1 = race_date.replace("May", "Maj").replace("Oct","Okt")
        formatted_race_date = datetime.datetime.strptime(race_date_1,'%Y-%b-%d')
        
        if formatted_race_date> mydate:
            i=0
            for k in table_row:
                Table_row_spilt = table_row[i].text.strip()
                
                billede =Table_row_spilt.split("\n")
                if not billede[0]  == "TV":
                        matches_for_the_day.append(f"{formatted_race_date.date().strftime('%Y-%b-%d'), billede[2].strip(), billede[6].strip()}")
                    
                i = i + 1

    channel = client.get_channel(1234600281854054482)
    if matches_for_the_day:
        matches_message = "\n".join( matches_for_the_day)
        matches_for_the_day.clear()
        await channel.send("<@&1234866967630839870>")
        await channel.send("**Todays matches:**")
        for part in split_message(matches_message.split("\n")):
            await channel.send(part)
    else:
        await channel.send("No matches for today.")
    
# asyncio.run(scrape_matches())