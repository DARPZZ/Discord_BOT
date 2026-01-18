from share import *
from datetime import datetime

def get_current_date():
    return datetime.today().strftime('%Y-%m-%d')
async def get_football_info():
    url = f"https://www.tvsporten.dk/api/fixtures/bydate?day={get_current_date()}&tzOffset=60&sportId=1"
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