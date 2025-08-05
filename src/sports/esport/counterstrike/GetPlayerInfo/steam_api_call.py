from dotenv import load_dotenv
load_dotenv()

import os
import requests
apiKey = os.getenv("steamAPIKey")
cs2ID = os.getenv("cs2ID")
steamID = os.getenv("steamID")
OWNED_GAMES = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"
GET_USER_STATS_FOR_GAME = "http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/"
RESOLVE_VANITY_URL = "https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/"
async def GetPlaytime(playerID):
    url = f"{OWNED_GAMES}?key={apiKey}&steamid={playerID}"
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
    
async def GetUserStatsForGame(playerID):
    url = f"{GET_USER_STATS_FOR_GAME}?appid={cs2ID}&key={apiKey}&steamid={playerID}"
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
    
async def CheckForVanityLink(playerID):

    url = f"{RESOLVE_VANITY_URL}?key={apiKey}&vanityurl={playerID}"
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
async def ProfileInformation(playerID):

    url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={apiKey}&steamids={playerID}"
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
    