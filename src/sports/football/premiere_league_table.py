from src.get_settings import read_settings_file as settings
from share import *
from enum import Enum
class international_football(Enum):
    champions_league = "Champions League"
    Europa_League = "Europa League"
    Nedrykning = "Nedrykning"
    
def add_space(number_of_space):
    space = "\u2003" * number_of_space
    return space

def add_feilds_to_embed(x,embedvar):
    team_name = x.find('a')['title']
    status = x.find_all('td',class_='text-center')
    matches_played = strip_text(status[1])
    matches_won = strip_text( status[2])
    matches_drawn = strip_text( status[3])
    matches_lost = strip_text (status[4])
    goals = strip_text (status[5])
    team_points = strip_text( status[6])
    embedvar.add_field(
        name="", value=f"**{team_name} {team_points}**\n Matches played: {matches_played}{add_space(1)}Matches won: {matches_won} {add_space(1)} Matches drawn: {matches_drawn} {add_space(1)} Matches lost: {matches_lost} \n Goals: {goals}", inline=False
        )
    
def strip_text(text_to_strip):
    return text_to_strip.text.strip()

async def scrape_matches():
    channel = client.get_channel(settings("footballl_premiere_league_table"))
    await channel.purge()
    url = "https://www.livescore.dk/premier-league/stilling/"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()
    soup = BeautifulSoup(text, 'html.parser')
    start_element = soup.find('table', class_="generic-table")
    nextt = start_element.find('tbody')
    nextt_childs = nextt.find_all('tr')
    for x in nextt_childs:
        if x.has_attr("title"):
            attribute = x['title']
            if attribute == international_football.champions_league.value:
                embedVar = discord.Embed( color=0x00ff00 )
            elif attribute == international_football.Europa_League.value: 
                embedVar = discord.Embed( color=0x0000ff )
            elif attribute == international_football.Nedrykning.value:
                embedVar = discord.Embed( color=0xff0000 )
        else:
            embedVar = discord.Embed(color=0xFFFFFF)
        add_feilds_to_embed(x,embedVar)
        
        await channel.send(embed=embedVar)