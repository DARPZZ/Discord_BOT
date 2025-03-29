import re
import requests
from datetime import datetime, timedelta
from share import *
url = "https://bo3.gg/matches/current"
headers = {'accept-language': 'da-DK,da;q=0.9,en-US;q=0.8,en;q=0.7',}
matches_for_the_day =[]
def show_rateing(table_row):
    rating = table_row.find("div", class_="c-table-cell-match-rating")
    rating_star = rating.find_all("i", class_="filled o-icon o-icon--star-1")
    if(len(rating_star)>=2):
        return True
    return False

def get_team_names(table_row):
    team_names = table_row.find_all('div', class_='team-name')
    first_team = team_names[0].text.strip()
    second_team = team_names[1].text.strip()
    return f"{first_team} VS {second_team}"

async def scrape_matches():
    channel = client.get_channel(1235813854580179125)
    await channel.purge(limit=25)
    await scrape_current_matches(channel)
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            text = await response.text()
    soup = BeautifulSoup(text, 'html.parser')
    mydate_time = datetime.now()
    my_date = mydate_time.date()
    my_date = my_date.strftime("%d-%m")
    mydate_string = str(my_date)
    locale.setlocale(locale.LC_TIME, "da_DK.UTF-8")
    matches = soup.find_all('div', class_= 'c-matches-group-rows')
    for match in matches:
        table_rows = match.find_all('div', class_='table-row table-row--upcoming')
        for table_row in table_rows:
            embedVar = discord.Embed( color=0x9D00FF, description="Match"  )
            ADate = table_row.find('a', class_='c-global-match-link table-cell')
            if ADate and show_rateing(table_row):
                href = ADate.get('href')
                date_match = re.search(r'\d{2}-\d{2}-\d{4}', href)
                match_date = date_match.group(0)
                match_date = match_date.split('-')
                match_date =  match_date[0] + '-' + match_date[1]
                if (match_date == mydate_string):
                    match_time = table_row.find('span', class_='time').text.strip()
                   
                    bo_type = table_row.find('span', class_='bo-type')
                    if(bo_type != None):
                        
                        bo_type_stripped = bo_type.text.strip()
                    else:
                        bo_type_stripped = "Unknown"
                    time_object = datetime.strptime(match_time, "%H:%M")

                    new_time_string = time_object.strftime("%H:%M")
                    new_time_string += timedelta(hours=1)
                    embedVar.add_field(name="**Teams:**", value=get_team_names(table_row), inline=False)
                    embedVar.add_field( name="**Time:**", value=new_time_string, inline=False)
                    embedVar.add_field(name="**BO:**", value=bo_type_stripped,inline=False)
                    #print(f"**Teams: ** {first_team} VS {second_team}\n**Time: ** {new_time_string}\n**BO: ** {bo_type_stripped}\n{'-'*60}\n")
                    await channel.send(embed=embedVar)
    return True
        


async def scrape_current_matches(channel):
    
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            text = await response.text()
    soup = BeautifulSoup(text, 'html.parser')
    matches = soup.find_all('div', class_= 'c-matches-group-rows')
    for match in matches:
        table_rows = match.find_all('div', class_='table-row table-row--current')
        for table_row in table_rows:
            embedVar = discord.Embed( color=0x9D00FF, description="Live Match")
            if show_rateing(table_row):
                #print(f"**Teams: ** {first_team} VS {second_team}\n**Score: **\n{'-'*60}\n")
                embedVar.add_field(name="**Teams: **",value= get_team_names(table_row),inline=False)
                embedVar.add_field(name="**Time: **", value="Live", inline=False)
                await channel.send(embed=embedVar)