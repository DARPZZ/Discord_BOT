import requests
from datetime import datetime, timedelta
import pytz
from share import *
from . import driver_standing
from . import team_standing
from src.get_settings import read_settings_file as settings
f1StartUrl = 'https://www.skysports.com/f1/'
def add_feilds(p_embedVar,p_name,p_value):
    p_embedVar.add_field(name=F"**{p_name}**",value=f"{p_value}",inline=False)

def get_channels(matchID):
    f1ID = settings("f1ID")
    for specificID in f1ID:
        if(matchID in specificID.keys()):
            return(specificID.get(matchID))
        
async def scrape_matches():

    channel = client.get_channel(get_channels("RaceID"))
    await channel.purge()
    url = f"{f1StartUrl}schedule-results"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()
    soup = BeautifulSoup(text, 'html.parser')
    races_all = soup.find('div', class_='f1-races')
    each_race = races_all.find_all('a', class_= 'f1-races__race')
    embedVar = discord.Embed( color=0x9D00FF,title="Important! all times are GMT+1")
    for element in each_race:
        sponsor = element.find('div',class_='f1-races__sponsor')
        if not sponsor:
            racename = element.find('h2',class_='f1-races__race-name')
            tbody = element.find('tbody')
            td = tbody.findChild()
            td_siblings = td.findNextSiblings()
            if td and td_siblings:
                embedVar.add_field(name="",value= f"**{racename.text.strip()}**",inline=False)
                embedVar.add_field(name="",value= td.text.strip()+ "\n",inline=False)
                for tdd in td_siblings:
                    embedVar.add_field(name="",value= tdd.text.strip()+ "\n",inline=False)
                await channel.send(embed=embedVar)
                return
async def Driver_team_standing():
    L = await asyncio.gather(
        driver_standing.scrape_driver_standing(f1StartUrl,add_feilds,get_channels("DriverID")),
        team_standing.scrape_team_standing(f1StartUrl,add_feilds,get_channels("TeamID")),
    )