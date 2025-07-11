import os
import json
import requests
from dotenv import load_dotenv
load_dotenv()
apiKey = os.getenv("steamAPIKey")
cs2ID = os.getenv("cs2ID")
steamID = os.getenv("steamID")
import asyncio
async def GetUserStatsForGame():
    url = f" http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid={cs2ID}&key={apiKey}&steamid={steamID}8"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            posts = response.json()
            
            return posts
        else:
            print('Error:', response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None
    
def get_hs_procentage(data,kills):
    stats_list = data['playerstats']['stats']
    stats = {s['name']: s['value'] for s in stats_list}
    total_kills_headshot = stats.get("total_kills_headshot")
    hs_procentage = (total_kills_headshot / kills) * 100
    return hs_procentage

def calculate_map_win_procentage(data):
    stats_list = data['playerstats']['stats']
    stats = {s['name']: s['value'] for s in stats_list}
    total_matches_played = stats.get("total_matches_played")
    total_matches_won = stats.get("total_matches_won")
    total_win_procentage = (total_matches_won / total_matches_played) * 100
    return total_win_procentage

def calculate_kd(data):
    stats_list = data['playerstats']['stats']
    stats = {s['name']: s['value'] for s in stats_list}
    kills = stats.get('total_kills')
    death = stats.get('total_deaths')
    kd = kills /death
    kd_dict = {
        "kills": kills,
        "deaths": death,
        "kd": kd
    }
    return kd_dict
        
async def get_info():
    data = await GetUserStatsForGame()
    kd_data = calculate_kd(data)
    hs_pro = get_hs_procentage(data,kd_data.get("kills"))
    calculate_map_win_procentage(data)
asyncio.run(get_info()) 
    