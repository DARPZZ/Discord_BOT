import requests
from datetime import datetime, timedelta
import pytz 
from share import *
matches_for_the_day =[]
current_driver_standing=[]



async def scrape_matches():
    url = "https://www.skysports.com/f1/schedule-results"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()
    soup = BeautifulSoup(text, 'html.parser')
    locale.setlocale(locale.LC_TIME, "da_DK.UTF-8")
    races = soup.find_all('div', class_= 'f1-races__race-inner')
    mydate = datetime.now()
    for race in races:
        table_row = race.find_all('tr',class_='standing-table__row')
        r_date = race.find_all('p', class_='f1-races__race-date')
        race_name = race.find_all('h2', class_= 'f1-races__race-name')
        race_name_split= race_name[0].text.strip()
        new_date_for_race = r_date[0].text.strip()[0:2]
        new_month_for_race = r_date[0].text.strip()[5:8]
        race_date =str(mydate.year) + "-" + new_month_for_race + "-" + new_date_for_race
        race_date_1 = race_date.replace("May", "Maj").replace("Oct","Okt")
        formatted_race_date = datetime.strptime(race_date_1,'%Y-%b-%d')
        if formatted_race_date> mydate:
            i=0
            for k in table_row:
                Table_row_spilt = table_row[i].text.strip()
                
                billede =Table_row_spilt.split("\n")
                
                if not billede[0]  == "TV":
                        uk_time_str = billede[6].strip()
                        uk_time = datetime.strptime(uk_time_str, '%H:%M')
                        uk_time += timedelta(hours=1)
                        danish_time = uk_time
                        danish_hour_str = danish_time.strftime('%H:%M')
                        matches_for_the_day.append(f"**Date:**\t{formatted_race_date.date().strftime('%d-%m-%Y')}\n**mode:**\t{billede[2].strip()} \n**Time:** \t{danish_hour_str}\n")
                        #print(f"**Date:**\t{formatted_race_date.date().strftime('%d-%m-%Y')}\n**mode:**\t{billede[2].strip()} \n**Time:** \t{danish_hour_str}\n")
                        if i % 5== 0:
                            #print(f"**Racename:** {race_name_split}\n{'-'*60}\n")
                            matches_for_the_day.append(f"**Racename:** {race_name_split}\n{'-'*60}\n")
                            await send_message(1234600281854054482,matches_for_the_day)
                            return(True)
                i = i + 1
    
async def scrape_driver_standing():
    url = "https://www.skysports.com/f1/standings"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()

    soup = BeautifulSoup(text, 'html.parser')
    
    table = soup.find('table', class_='standing-table__table')
    
    if table:
        rows = table.find_all('tr')[1:]
        for row in rows:
            cells = row.find_all('td')
            
           
            place = cells[0].text.strip()
            name = cells[1].text.strip()
            country = cells[2].text.strip()  
            team = cells[3].text.strip()     
            points = cells[4].text.strip()  
            current_driver_standing.append(f"**Name:** {name}\n**Place:** {place}\n**Country:** {country}\n**Team:** {team}\nPoints: {points}\n\n")
        await send_message(1297902739698880573,current_driver_standing)
    
    
    
async def send_message(Channel_id,match_liste):
    channel = client.get_channel(Channel_id)
    await channel.purge(limit=25)
    if matches_for_the_day:
        matches_message = "\n".join( match_liste)
        matches_for_the_day.clear()
        await channel.send("<@&1234866967630839870>")
        await channel.send("**Todays matches:**")
        for part in split_message(matches_message.split("\n")):
            await channel.send(part)
    else:
        await channel.send("No matches for today.")


    

    
