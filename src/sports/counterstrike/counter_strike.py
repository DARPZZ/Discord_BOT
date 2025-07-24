import asyncio
import re
from tracemalloc import start
import requests
from datetime import datetime, timedelta
from share import *
ERROR_MESSAGE = f"Unable to get data for"
DISCORDCHANNEL = 1235813854580179125
def get_current_date():
    return datetime.today().strftime('%Y-%m-%d')

def eror_message(specific_error):
    return f"{ERROR_MESSAGE} {specific_error}"

async def get_counter_strike_pro_info_upcomming():
    url = f"https://api.bo3.gg/api/v2/matches/upcoming?date={get_current_date()}&utc_offset=7200&filter[discipline_id][eq]=1"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            matches = response.json()
            return matches
        else:
            print('Error:', response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None
    
async def get_counter_strike_pro_info_live():
    url = f"https://api.bo3.gg/api/v2/matches/live?date={get_current_date()}&utc_offset=7200&filter%5Bdiscipline_id%5D%5Beq%5D=1"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            matches = response.json()
            return matches
        else:
            print('Error:', response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None
    
def get_team_names(element):
    try:
        team_names = element.get('slug')
        pattern = re.compile(r"^([a-z0-9\-_]+)-vs-([a-z0-9\-_]+?)(?:-\d{2}-\d{2}-\d{4})?$", re.IGNORECASE)
        for line in team_names.strip().splitlines():
            match = pattern.match(line)
            if match:
                team1 = match.group(1).replace("-", " ")
                team2 = match.group(2).replace("-", " ")
                return f"{team1} VS {team2}"
    except:
        return eror_message("the team names")   
    
def get_odds(element):
    try:
        bet_updates = element.get('bet_updates')
        if bet_updates:
            coeff_team_1 = bet_updates.get('team_1')
            odds_team_1  = coeff_team_1.get('coeff')
            coeff_team_2  = bet_updates.get('team_2')
            odds_team_2  = coeff_team_2.get('coeff')
            return f"{odds_team_1} - {odds_team_2}"
    except:
        return eror_message("odds") 
    
def get_start_date(element):
    try:
        start_date_str = element.get('start_date')
        start_date = datetime.strptime(start_date_str, '%Y-%m-%dT%H:%M:%S.%f%z')
        start_date_plus_2h = start_date + timedelta(hours=2)
        start_date_only = start_date_plus_2h.strftime('%Y-%m-%d %H:%M')
        return start_date_only
    except:
        return eror_message("start date")
    
async def show_info_for_upcomming_matches(channel):
    data = await get_counter_strike_pro_info_upcomming()
    match_data = data['data']['tiers']['high_tier']['matches']
    for element in match_data:
        stars = element.get('stars')
        if (stars < 1):
            continue
        embedVar = discord.Embed( color=0xFF9DFF,title=f"{get_start_date(element)}")
        team_name = get_team_names(element)
        odds =  get_odds(element)
        bo_type = element.get('bo_type')
        embedVar.add_field(name="**Teams: **",value= team_name,inline=False)
        embedVar.add_field(name="**Odds: **",value= odds,inline=True)
        embedVar.add_field(name="**BO: **",value= bo_type,inline=True)
        await channel.send(embed=embedVar)
        
async def show_info_for_live_matches(channel):
    data = await get_counter_strike_pro_info_live()
    match_data = data['data']
    for element in match_data:
        stars = element.get('stars')
        if stars <2:
            continue
        embedVar = discord.Embed( color=0x9DFF00,title=f"**Live**")
        team_name = get_team_names(element)
        team1_score = element.get('team1_score')
        team2_score =element.get('team2_score')
        
        embedVar.add_field(name="**Teams**: ",value=team_name)
        embedVar.add_field(name="**Score**: ",value=f"{team1_score} - {team2_score} ")
        await channel.send(embed=embedVar)
        
async def show_info():
    channel = client.get_channel(DISCORDCHANNEL)
    await channel.purge(limit=25)
    await show_info_for_live_matches(channel)
    await show_info_for_upcomming_matches(channel)
    return True
