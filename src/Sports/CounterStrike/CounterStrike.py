import re
import requests
from datetime import datetime, timedelta
from . import CounterStrikeCurrentMatches
from share import *
from ...SendIfNoData import sendMessageForNoData
url = "https://bo3.gg/matches/current"
headers = {'accept-language': 'da-DK,da;q=0.9,en-US;q=0.8,en;q=0.7',}
matches_for_the_day =[]
async def  show_rateing(table_row):
    rating = table_row.find("div", class_="c-table-cell-match-rating")
    if rating != None:
        rating_star = rating.find_all("i", class_="filled o-icon o-icon--star-1")
        if(len(rating_star)>=2):
            return True
    return False

async def get_team_names(table_row):
    team_names = table_row.find_all('div', class_='team-name')
    first_team = team_names[0].text.strip()
    second_team = team_names[1].text.strip()
    return f"{first_team} VS {second_team}"

def get_current_date():
    mydate_time = datetime.now()
    my_date = mydate_time.date()
    my_date = my_date.strftime("%d-%m")
    return my_date

def get_bo_type(table_row):
    bo_type = table_row.find('span', class_='bo-type')
    if(bo_type != None):
        bo_type_stripped = bo_type.text.strip()
    else:
        bo_type_stripped = "Unknown"
    return bo_type_stripped

async def scrape_matches():
    channel = client.get_channel(1235813854580179125)
    await channel.purge(limit=25)
    await CounterStrikeCurrentMatches.scrape_current_matches(channel,headers,url,show_rateing,get_team_names)
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            text = await response.text()
    soup = BeautifulSoup(text, 'html.parser')
    mydate_string = str(get_current_date())
    locale.setlocale(locale.LC_TIME, "da_DK.UTF-8")
    matches = soup.find_all('div', class_= 'c-matches-group-rows')
    for match in matches:
        table_rows = match.find_all('div', class_='table-row table-row--upcoming')
        for table_row in table_rows:
            embedVar = discord.Embed( color=0x9D00FF, description="Match"  )
            ADate = table_row.find('a', class_='c-global-match-link table-cell')
            if ADate and await show_rateing(table_row):
                href = ADate.get('href')
                date_match = re.search(r'\d{2}-\d{2}-\d{4}', href)
                match_date = date_match.group(0)
                match_date = match_date.split('-')
                match_date =  match_date[0] + '-' + match_date[1]
                if (match_date == mydate_string):
                    match_time = table_row.find('span', class_='time').text.strip()
                    bo_type_stripped = get_bo_type(table_row)
                    time_object = datetime.strptime(match_time, "%H:%M")
                    time_object += timedelta(hours=2)
                    new_time_string = time_object.strftime("%H:%M")
                    embedVar.add_field(name="**Teams:**", value=await get_team_names(table_row), inline=False)
                    embedVar.add_field( name="**Time:**", value=new_time_string, inline=False)
                    embedVar.add_field(name="**BO:**", value=bo_type_stripped,inline=False)
                    matches_for_the_day.append(embedVar)
                    await channel.send(embed=embedVar)
    if (len(matches_for_the_day)<=0):
        await sendMessageForNoData(discord,channel)
    return True
        
