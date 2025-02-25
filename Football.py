import datetime
import aiohttp
from share import *
from discord.ext import tasks
matches_for_the_day =[]
date_string =''
first_team_win_odss=""
draw_odss=""
second_team_win_odss=""
all_odds = ""
no_odds =""

async def add_feilds(embedVar,teams,tid,real_league,kanal):
    embedVar.add_field(name="Teams:", value=teams, inline=False)
    embedVar.add_field(name="Tid:", value=tid, inline=False)
    embedVar.add_field(name="Liga:", value=real_league, inline=False)
    embedVar.add_field(name="Odds:", value=all_odds, inline=False)
    embedVar.add_field(name="Kanal:", value=kanal, inline=False)
    embedVar.add_field(name="",value=f"\n{'-'*60}\n", inline=False)

async def calculate_odds(football_match,teams):
    global all_odds
    global no_odds
    global first_team_win_odss
    global draw_odss
    global second_team_win_odss
    first_team__name = teams.split("-")[0]
    second_team__name = teams.split("-")[1]
    odss = football_match.find('ul', class_='odds')
    if odss != None:
        odss_value = odss.find_all('span', class_='value')
        first_team_win_odss = first_team__name + " " + odss_value[0].text.strip()
        draw_odss = "Draw" + " " + odss_value[1].text.strip()
        second_team_win_odss = second_team__name + " " + odss_value[2].text.strip()
        
        all_odds = f"{first_team_win_odss}\u2003{draw_odss}\u2003{second_team_win_odss}"

    else:
        all_odds ="No odds or the match is live"
    
async def scrape_matches():
    date_string =""
    channel = client.get_channel(1234600317090529392)
    await channel.purge()
    loop_bool = True
    url = "https://www.livescore.dk/fodbold-i-tv/"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()
    soup = BeautifulSoup(text, 'html.parser')
    todays_matches = soup.find('div', class_='tv-table tv-table--football')
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
        embedVar = discord.Embed( color=0x00ff00 )
        embedVar.set_footer(text="Oddsne er fra LeoVegas",icon_url=None)
        match = football_match.find_next_sibling()
        if match == None:
            break
        football_match = match
        if match.find('div', class_='date'):
            loop_bool = False
            break
        teams = football_match.find('span', class_='text').text.strip()
        await calculate_odds(football_match,teams)
        tid = football_match.find('div', class_='time').text.strip()
        kanal = football_match.find('div', class_='chanels')
        img_tag = kanal.find('img')
        kanal = img_tag.get('alt', 'No alt attribute') if img_tag else 'No image found'
        league = football_match.find('div', class_='league')
        real_league = league.find('span', class_='text').text.strip() 
        await add_feilds(embedVar,teams,tid,real_league,kanal)
        await channel.send(embed=embedVar)
    return True