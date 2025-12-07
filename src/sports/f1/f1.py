from src.helpers.connection import connection
from share import *
from src.sports.f1.driver_standing import driver_standing
from src.sports.f1.team_standing import team_standing
class f1:
    f1StartUrl = 'https://www.skysports.com/f1/'
    def __init__(self,settings):
        self.connection = connection(aiohttp,BeautifulSoup)
        self.settings = settings
        self.team_standing = team_standing()
        self.driver_standing = driver_standing()
        
    def add_feilds(self,p_embedVar,p_name,p_value):
        p_embedVar.add_field(name=F"**{p_name}**",value=f"{p_value}",inline=False)

    def get_channels(self,matchID):
        f1ID = self.settings("f1ID")
        for specificID in f1ID:
            if(matchID in specificID.keys()):
                return(specificID.get(matchID))
    async def scrape_matches(self):
        channel = client.get_channel(self.get_channels("RaceID"))
        await channel.purge()
        url = f"{self.f1StartUrl}schedule-results"
        data = await self.connection.create_connection(url)
        races_all = data.find('div', class_='f1-races')
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
    async def Driver_team_standing(self):
        L = await asyncio.gather(
            self.driver_standing.scrape_driver_standing(self.f1StartUrl,self.add_feilds,self.get_channels("DriverID")),
            self.team_standing.scrape_team_standing(self.f1StartUrl,self.add_feilds,self.get_channels("TeamID")),
        )