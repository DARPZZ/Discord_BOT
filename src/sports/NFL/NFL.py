
from share import *
from bs4 import BeautifulSoup
from src.get_settings import read_settings_file as settings
def remove_nfl_team_tag(element):
    newelement = element.split(':')
    newelement = newelement[1].strip()
    return newelement 

async def scrape_nfl_mathces():
    channel = client.get_channel(settings("NFLID"))
    await channel.purge()
    url = "https://sport.tv2.dk/amerikansk-fodbold/nfl/sendeplan"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()
        soup = BeautifulSoup(text, 'html.parser')
        grid_gutter = soup.find('section',class_='tc_tvlisting__group')
        tc_tvlistings = grid_gutter.find_all('article',class_="tc_tvlisting")
        for element in tc_tvlistings:
            embed_var = discord.Embed( color=0x89CFF0)
            aria_label = element['aria-label']
            team_names = remove_nfl_team_tag(aria_label)
            
            timestamp = element.find('time',class_='tc_timestamp').text.strip()
            embed_var.add_field(name="**Time: **",value=timestamp)
            embed_var.add_field(name="**Teams: **",value=team_names)
            await channel.send(embed=embed_var)
