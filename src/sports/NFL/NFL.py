
from share import *
from bs4 import BeautifulSoup

class NFL:
    def __init__(self,settings):
        self.url = "https://sport.tv2.dk/amerikansk-fodbold/nfl/sendeplan"
        self.settings = settings
        
    def remove_nfl_team_tag(self,element):
        newelement = element.split(':')
        newelement = newelement[1].strip()
        return newelement 

    async def scrape_nfl_mathces(self):
        channel = client.get_channel(self.settings("NFLID"))
        await channel.purge()
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as response:
                text = await response.text()
            soup = BeautifulSoup(text, 'html.parser')
            grid_gutter = soup.find('section',class_='tc_tvlisting__group')
            tc_tvlistings = grid_gutter.find_all('article',class_="tc_tvlisting")
            for element in tc_tvlistings:
                embed_var = discord.Embed( color=0x89CFF0)
                aria_label = element['aria-label']
                team_names = self.remove_nfl_team_tag(aria_label)
                timestamp = element.find('time',class_='tc_timestamp').text.strip()
                embed_var.add_field(name="**Time: **",value=timestamp)
                embed_var.add_field(name="**Teams: **",value=team_names)
                await channel.send(embed=embed_var)
