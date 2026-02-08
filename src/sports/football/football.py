from src.sports.football.football_api import get_football_info
from src.helpers.feilds import feilds
from share import *
from datetime import datetime
matches_for_the_day =[]
date_string =''
first_team_win_odss=""
draw_odss=""
second_team_win_odss=""
all_odds = ""
no_odds =""
class football:
    def __init__(self,settings):
        self.settings = settings
        self.embedVar = discord.Embed( color=0x00ff00 )
        self.feilds_obj = feilds(self.embedVar)

        
    async def add_feilds(self,teams,tid,real_league,kanal,odds):
        self.feilds_obj.generate_feilds("Teams:",teams)
        self.feilds_obj.generate_feilds("Tid:",tid)
        self.feilds_obj.generate_feilds("Liga:",real_league)
        self.feilds_obj.generate_feilds("Odds:",odds)
        self.feilds_obj.generate_feilds("Kanal(er):",kanal)
        self.feilds_obj.generate_feilds("",f"\n{'-'*60}\n")
        
    
    async def scrape_matches(self):
        football_settings = self.settings("football")
        allowed_channels = football_settings["fotball_allowed_channels"]
        allowed_leagues = football_settings["football_allowed_leagues"]
        channel = client.get_channel(football_settings["footballID"])
        await channel.purge()
        data = await get_football_info()
        newFixtures = data[0]['newFixtures']
        for fixure in newFixtures:
            allow_send_message = False
            self.embedVar.clear_fields()
            date = fixure['date']
            home_team = fixure['home_team']
            visiting_team = fixure['visiting_team']
            league = fixure['league']
            odds_1 = fixure['odds_1']
            odds_x = fixure['odds_x']
            odds_2 = fixure['odds_2']
            channels = fixure['channels']
            channel_string = ""
            for x in channels:
                channel_name = x['name']
                if channel_name in allowed_channels and league in allowed_leagues:
                    allow_send_message = True
                    channel_string = f"{channel_string}  {channel_name} \n"
            dt = datetime.fromisoformat(date.replace("Z", "+00:00"))
            time = dt.strftime("%H:%M")
            odds = f"{odds_1}x - {odds_x}x - {odds_2}x"
            teams = f"{home_team} VS {visiting_team}"
            if (allow_send_message):
                await self.add_feilds(teams,time,league,channel_string,odds)
                await channel.send(embed=self.embedVar)
        return True
