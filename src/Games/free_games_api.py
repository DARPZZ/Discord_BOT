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