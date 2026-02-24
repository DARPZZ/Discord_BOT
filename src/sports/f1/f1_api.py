import requests
from datetime import datetime
async def get_f1_info():
    url = f"https://f1api.dev/api/{datetime.now().year}"
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