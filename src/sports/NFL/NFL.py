
from share import *
from bs4 import BeautifulSoup
import src.helpers.connection as connection
import src.helpers.feilds as feilds
class NFL:
    def __init__(self,settings):
        self.embed_var = discord.Embed( color=0x89CFF0)
        self.url = "https://sport.tv2.dk/amerikansk-fodbold/nfl/sendeplan"
        self.settings = settings
        self.feilds_obj = feilds.feilds(self.embed_var)
        
    def remove_nfl_team_tag(self,element):
        newelement = element.split(':')
        newelement = newelement[1].strip()
        return newelement 

    async def scrape_nfl_mathces(self):
        channel = client.get_channel(self.settings("NFLID"))
        await self.feilds_obj.clear_feilds(channel)
        connection_obj = connection.connection(aiohttp,BeautifulSoup)
        data = await connection_obj.create_connection(self.url)
        grid_gutter = data.find('section',class_='tc_tvlisting__group')
        tc_tvlistings = grid_gutter.find_all('article',class_="tc_tvlisting")
        for element in tc_tvlistings:
            self.embed_var.clear_fields()
            aria_label = element['aria-label']
            team_names = self.remove_nfl_team_tag(aria_label)
            timestamp = element.find('time',class_='tc_timestamp').text.strip()
            self.feilds_obj.generate_feilds("**Time: **",timestamp)
            self.feilds_obj.generate_feilds("**Teams: **",team_names)
            await channel.send(embed=self.embed_var)
