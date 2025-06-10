import requests
from datetime import datetime, timedelta
import pytz 
from share import *

f1StartUrl = 'https://www.skysports.com/f1/'
def add_feilds(p_embedVar,p_name,p_value):
    p_embedVar.add_field(name=F"**{p_name}**",value=f"{p_value}",inline=False)
    
async def scrape_matches():
    
    channel = client.get_channel(1234600281854054482)
    await channel.purge()
    url = f"{f1StartUrl}schedule-results"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()
    soup = BeautifulSoup(text, 'html.parser')
    locale.setlocale(locale.LC_TIME, "da_DK.UTF-8")
    races = soup.find_all('div', class_='f1-races__race-inner')
    mydate = datetime.now()
    for race in races:
        table_row = race.find_all('tr', class_='standing-table__row')
        r_date = race.find_all('p', class_='f1-races__race-date')
        race_name = race.find_all('h2', class_='f1-races__race-name')
        race_name_split = race_name[0].text.strip()
        new_date_for_race = r_date[0].text.strip()[0:2]
        new_month_for_race = r_date[0].text.strip()[5:8]
        race_date = str(mydate.year) + "-" + new_month_for_race + "-" + new_date_for_race
        race_date_1 = race_date.replace("May", "Maj").replace("Oct", "Okt")
        formatted_race_date = datetime.strptime(race_date_1, '%Y-%b-%d')
        embedVar = discord.Embed( color=0x9D00FF)
        add_feilds(embedVar,"Date: ",f"{formatted_race_date.date().strftime('%d-%m-%Y')}\n")
        
        if formatted_race_date > mydate:
            i = 0
            for k in table_row:
                table_row_split = table_row[i].text.strip()
                billede = table_row_split.split("\n")
                
                if not billede[0] == "TV":
                    uk_time_str = billede[6].strip()
                    uk_time = datetime.strptime(uk_time_str, '%H:%M')
                    uk_time += timedelta(hours=1)
                    danish_time = uk_time
                    danish_hour_str = danish_time.strftime('%H:%M')
                    add_feilds(embedVar,"Mode: ",billede[2].strip())
                    add_feilds(embedVar,"Time: ",danish_hour_str)
                    add_feilds(embedVar, " "," ")
                    if i % 5 == 0:
                        add_feilds(embedVar,"Race country: ", f"{race_name_split}\n" )
                        await channel.send(embed=embedVar)
                        
                        return

                i += 1


async def scrape_driver_standing():
    url = f"{f1StartUrl}/standings"
    channel = client.get_channel(1297902739698880573)
    await channel.purge(limit=25)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()

    soup = BeautifulSoup(text, 'html.parser')
    
    table = soup.find('table', class_='standing-table__table')
    
    if table:
        rows = table.find_all('tr')[1:]
        for row in rows:
            embedVar = discord.Embed( color=0x9D00FF)
            cells = row.find_all('td')
            name = cells[1].text.strip()
            country = cells[2].text.strip()  
            team = cells[3].text.strip()     
            points = cells[4].text.strip()  
            add_feilds(embedVar,"Driver name: ", name)
            add_feilds(embedVar,"Country: ", country)
            add_feilds(embedVar,"Team: ", team)
            add_feilds(embedVar,"Points: ", points)
            await channel.send(embed=embedVar)
    

    
        
async def scrape_team_standing():
    channel = client.get_channel(1381729288340111551)
    await channel.purge()
    url = f"{f1StartUrl}/standings"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()
            
    soup = BeautifulSoup(text, 'html.parser')
    table = soup.find_all('table', class_='standing-table__table')
    if table:
        team_table = table[1]
        standing_table__row = team_table.find_all('tr', class_='standing-table__row')
        for element in standing_table__row:
            embedVar = discord.Embed( color=0x9D00FF)
            team_name = element.find('td', class_='standing-table__cell standing-table__cell--name')
            if team_name != None:
                team_points = team_name.findNextSibling()
                team_name_text = team_name.text.strip()
                team_points_text = team_points.text.strip()
                add_feilds(embedVar,"Name: ", team_name_text)
                add_feilds(embedVar,"Points: ", team_points_text)
                await channel.send(embed=embedVar)

    