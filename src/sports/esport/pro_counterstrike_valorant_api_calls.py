from share import *
from datetime import datetime, timedelta

def get_current_date():
    return datetime.today().strftime('%Y-%m-%d')

async def get_counter_strike_valorant_pro_info_upcomming(id):
    url = f"https://api.bo3.gg/api/v2/matches/upcoming?date={get_current_date()}&utc_offset=7200&filter[discipline_id][eq]={id}"
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
    
async def get_counter_strike_valorant_pro_info_live(id):
    url = f"https://api.bo3.gg/api/v2/matches/live?date={get_current_date()}&utc_offset=7200&filter%5Bdiscipline_id%5D%5Beq%5D={id}"
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

async def get_counter_strike_valorant_stream_coverage(slug):
    url = f"https://api.bo3.gg/api/v1/matches/{slug}?scope=show-match&stream_language=en"
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
    

