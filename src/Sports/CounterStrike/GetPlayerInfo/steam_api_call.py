from dotenv import load_dotenv
load_dotenv()

import os
import requests
apiKey = os.getenv("steamAPIKey")
cs2ID = os.getenv("cs2ID")
steamID = os.getenv("steamID")
OWNED_GAMES = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"
GET_USER_STATS_FOR_GAME = "http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/"
async def GetPlaytime(playerID):
    url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={apiKey}&steamid={playerID}"
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

    url = f"https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/?key={apiKey}&vanityurl={playerID}"
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