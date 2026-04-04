from src.helpers.connection import connection
from share import *
from src.sports.f1.driver_standing import driver_standing
from src.sports.f1.team_standing import team_standing
from src.sports.f1.f1_api import get_f1_info
import datetime
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
        f1ID = self.get_f1_settings_id()['f1ID']
        for specificID in f1ID:
            if(matchID in specificID.keys()):
                return(specificID.get(matchID))
            
    def get_f1_settings_id(self):
        return self.settings("f1")
    
    async def scrape_matches(self):
        channel = client.get_channel(self.get_channels("RaceID"))
        await channel.purge()
        data = await get_f1_info()
        if not data:
            return
        races = data['races']
        for first_race in races:
            raceName = first_race['raceName']
            schedule = first_race['schedule']
            embedvar  = discord.Embed( color=0x00ff00,title=raceName)
            events = [
                {"type": "fp1", "data": schedule["fp1"]},
                {"type": "fp2", "data": schedule["fp2"]},
                {"type": "fp3", "data": schedule["fp3"]},
                {"type": "sprintQualy", "data": schedule["sprintQualy"]},
                {"type": "sprintRace", "data": schedule["sprintRace"]},
                {"type": "qualy", "data": schedule["qualy"]},
                {"type": "race", "data": schedule["race"]},
            ]
            
            format_code = "%Y-%m-%d"
            current_date = datetime.datetime.now().date()  
            future_datetime = datetime.datetime.strptime(events[0]['data']['date'], format_code).date()

            if future_datetime < current_date:
                continue
            for event in events:
                if (event['data']['date'] == None):
                    continue
                correct_time = event['data']['time'].replace('Z','')
                new_time = (
                    datetime.datetime.strptime(correct_time, "%H:%M:%S")
                    + datetime.timedelta(hours=1)
                ).strftime("%H:%M:%S")
                date_and_time = f"{event['data']['date']} -  {new_time}"
                embedvar.add_field(name= event["type"], value= date_and_time, inline= False)
            await channel.send(embed=embedvar)
            break
    async def Driver_team_standing(self):
        L = await asyncio.gather(
            self.driver_standing.scrape_driver_standing(self.f1StartUrl,self.add_feilds,self.get_channels("DriverID")),
            self.team_standing.scrape_team_standing(self.f1StartUrl,self.add_feilds,self.get_channels("TeamID")),
        )