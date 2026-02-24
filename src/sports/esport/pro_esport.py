import re
ERROR_MESSAGE = f"Unable to get data for"
from datetime import datetime, timedelta
team_name_dict = {}
def eror_message(specific_error):
    return f"{ERROR_MESSAGE} {specific_error}"

def get_maps(element):
    map_array = []
    maps = element.get('games')
    if maps == None:
        return ["We could not get any map data for this match"]
    for mapp in maps:
        map_name = mapp.get('map_name')
        if map_name == None:
            map_name = "Unknown"
        map_status = mapp.get('status')
        full_map = f"Map name: {map_name} - Map status: {map_status}"
        map_array.append(full_map)
    return map_array

def get_team_names(data):
    try: 
        team_name_data = data['included']['teams']
        for team_id, team_info in team_name_data.items():
            team_info_name = team_info.get('name')
            team_name_dict[team_id]= team_info_name
        return team_name_dict
    except:
        return None
    
async def place_team_names_values(data,element):
    data = get_team_names(data)
    if(data is None):
        return "Could not find the team names"
    first_team_id = element.get('team1_id')
    second_team_id = element.get('team2_id') 
    team_names = f"{data.get(str(first_team_id))} VS {data.get(str(second_team_id))}"
    return team_names

async def get_tournament_info(data,tournament_dict):
    tournament_dict.clear()
    tournamentdata = data['included']['tournaments']
    for element in tournamentdata.values():
        tournament_id = element.get('id')
        tournament_name = element.get('name')
        tournament_prize_pool = element.get('prize')
        tournament_dict[tournament_id]={
            "tournament_name" : tournament_name,
            "tournament_prize_pool": tournament_prize_pool
        }
        
async def place_tournament_info(element,data,tournament_dict):
    await get_tournament_info(data,tournament_dict)
    tournament_element = element.get('tournament')
    if (tournament_element):
        tournament_info = tournament_dict.get(int(tournament_element))
        tournament_name = tournament_info.get('tournament_name')
        tournament_price_pool = tournament_info.get('tournament_prize_pool')
        if (tournament_price_pool != None ):
            format_type = "{:,}"
            tournament_price_pool = format_type.format(tournament_price_pool).replace(",",".")
        return[tournament_name,tournament_price_pool]
   
async def get_odds(element):
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

async def get_stream_coverage(slug, api_call):
    try:
        data = await api_call.get_counter_strike_valorant_stream_coverage(slug)
        stream_data = data['streams']
        stream_dict = {}
        for x in stream_data:
            stream_url = x.get('raw_url')
            language = x.get('language')
            viewers = x.get('viewers_number')
            if language == "en":
                stream_dict_len = len(stream_dict)
                if (stream_dict_len > 5):
                    return stream_dict
                stream_dict[stream_url] = viewers
         
        return stream_dict
    except Exception as e:
        print(f"get_stream_coverage error: {e}")
        return {}
