from src.helpers.connection import connection
from src.helpers.feilds import feilds
from share import *
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
        self.url = "https://www.livescore.dk/fodbold-i-tv/"
        
    async def add_feilds(self,teams,tid,real_league,kanal):
        self.feilds_obj.generate_feilds("Teams:",teams)
        self.feilds_obj.generate_feilds("Tid:",tid)
        self.feilds_obj.generate_feilds("Liga:",real_league)
        self.feilds_obj.generate_feilds("Odds:",self.all_odds)
        self.feilds_obj.generate_feilds("Kanal:",kanal)
        self.feilds_obj.generate_feilds("",f"\n{'-'*60}\n")
        
    async def calculate_odds(self,football_match,teams):
        try:
            first_team__name = teams.split("-")[0]
            second_team__name = teams.split("-")[1]
            odss = football_match.find('ul', class_='odds')
            if odss != None:
                odss_value = odss.find_all('span', class_='value')
                first_team_win_odss = first_team__name + " " + odss_value[0].text.strip()
                draw_odss = "Draw" + " " + odss_value[1].text.strip()
                second_team_win_odss = second_team__name + " " + odss_value[2].text.strip()
                
                self.all_odds = f"{first_team_win_odss}\u2003{draw_odss}\u2003{second_team_win_odss}"

            else:
                all_odds ="No odds or the match is live"
        except:
            all_odds = "Could not calculate all odds"
            
    def get_channel(self,football_match):
        kanal = football_match.find('div', class_='chanels')
        img_tag = kanal.find('img')
        kanal = img_tag.get('alt', 'No alt attribute') if img_tag else 'No image found'
        return kanal
    
    def get_league(self,football_match):
        league = football_match.find('div', class_='league')
        real_league = league.find('span', class_='text').text.strip() 
        return real_league
    
    async def scrape_matches(self):

        channel = client.get_channel(self.settings("footballID"))
        await channel.purge()
        loop_bool = True
        connection_obj = connection(aiohttp,BeautifulSoup)
        data = await connection_obj.create_connection(url=self.url)
        todays_matches = data.find('div', class_='tv-table tv-table--football')
        if todays_matches == None:
            no_matches_embed = discord.Embed( color=0x00ff00,description="There is no matches today")
            await channel.send(embed=no_matches_embed)
            return
        football_match = todays_matches.find_next()
        date = football_match.find('div', class_='date')
        if date != None:
            date_string = date.text.strip()
        await channel.send(content=f"Fodbold kampe {date_string}")  
        while loop_bool:
            self.embedVar.clear_fields()
            self.embedVar.set_footer(text="Oddsne er fra LeoVegas",icon_url=None)
            match = football_match.find_next_sibling()
            if match == None:
                break
            football_match = match
            if match.find('div', class_='date'):
                loop_bool = False
                break
            teams = football_match.find('span', class_='text').text.strip()
            await self.calculate_odds(football_match,teams)
            tid = football_match.find('div', class_='time').text.strip()
            await self.add_feilds(teams,tid,self.get_league(football_match),self.get_channel(football_match))
            await channel.send(embed=self.embedVar)
        return True