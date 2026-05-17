import requests
async def get_data(platform):
    url = f"https://www.gamerpower.com/api/giveaways?platform={platform}&type=game"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            matches = response.json()
            return matches
        else:
            print('Error:', response.status_code)
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None
async def get_app_id(game_name):
    url = f"https://store.steampowered.com/api/storesearch/?term={game_name}&cc=us&l=en"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            matches = response.json()
            return matches
        else:
            print('Error:', response.status_code)
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None
