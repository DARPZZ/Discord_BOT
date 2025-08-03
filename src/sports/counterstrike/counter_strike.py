import re
from src.sports.counterstrike.pro_counterstrike_api_calls import get_counter_strike_pro_info_live,get_counter_strike_pro_info_upcomming,get_counterr_strike_stream_coverage
from datetime import datetime, timedelta
from share import *
import src.sports.counterstrike.create_counter_strike_embeds as  create_counter_strike_embeds
from src.get_settings import read_settings_file as settings

ERROR_MESSAGE = f"Unable to get data for"
tournament_dict = {}

def eror_message(specific_error):
    return f"{ERROR_MESSAGE} {specific_error}"

def get_maps(element):
    map_array = []
    maps = element.get('games')
    for mapp in maps:
        map_name = mapp.get('map_name')
        if map_name == None:
            map_name = "Unknown"
        map_status = mapp.get('status')
        full_map = f"Map name: {map_name} - Map status: {map_status}"
        map_array.append(full_map)
    return map_array

async def get_tournament_info(data):
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
async def place_tournament_info(element,data):
    await get_tournament_info(data)
    tournament_element = element.get('tournament')
    if (tournament_element):
        tournament_info = tournament_dict.get(int(tournament_element))
        tournament_name = tournament_info.get('tournament_name')
        tournament_price_pool = tournament_info.get('tournament_prize_pool')
        return[tournament_name,tournament_price_pool]
    
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

async def get_stream_coverage(slug):
    try:
        data = await get_counterr_strike_stream_coverage(slug)
        stream_data = data['streams']
        stream_dict= {}
        stream_dict.clear()
        for x in stream_data:
            stream_url = x.get('raw_url')
            official = x.get('official')
            language = x.get('language')
            viewers = x.get('viewers_number')
            if(official and language == "en"):
                stream_dict[stream_url] = viewers 
        return stream_dict
    except:
        return "Could not get stream coverage"
    
async def show_info_for_upcomming_matches(channel):
    try:
        data = await get_counter_strike_pro_info_upcomming()
        if (data):
            match_data = data['data']['tiers']['high_tier']['matches']
            for element in match_data:
                stars = element.get('stars')
                if (stars <= 2):
                    continue
                tournament_info = await place_tournament_info(element,data)
                embedVar = discord.Embed( color=0xFF9DFF,title=f"{get_start_date(element)}")
                team_name = get_team_names(element)
                odds =  get_odds(element)
                bo_type = element.get('bo_type')
                slug = element.get('slug')
                create_counter_strike_embeds.create_upcomming_matches_enmed(embedVar,team_name,odds,bo_type,tournament_info[0],tournament_info[1])
                streams = await get_stream_coverage(slug)
                create_counter_strike_embeds.create_streams_embed(streams,embedVar)
                await channel.send(embed=embedVar)
    except Exception :
        await channel.send("We could not find any high tier matches")

async def show_info_for_live_matches(channel):
    data = await get_counter_strike_pro_info_live()
    if(data):
        match_data = data['data']
        for element in match_data:
            stars = element.get('stars',0)
            if (stars <= 2):
                continue
            tournament_info = await place_tournament_info(element,data)
            embedVar = discord.Embed( color=0x9DFF00,title=f"**Live**")
            team_name = get_team_names(element)
            team1_score = element.get('team1_score')
            team2_score =element.get('team2_score')
            create_counter_strike_embeds.create_live_matches_enmed(embedVar,team_name,team1_score,team2_score,tournament_info[0],tournament_info[1])
            maps = get_maps(element)
            embedVar.add_field(name=f"",value="**Maps: **",inline=False)
            for mapp in maps:
                embedVar.add_field(name=f"",value=mapp,inline=False)
            slug = element.get('slug')
            streams = await get_stream_coverage(slug)
            await create_counter_strike_embeds.create_streams_embed(streams,embedVar)
            await channel.send(embed=embedVar)
            
async def show_info():
    channel = client.get_channel(settings("proPlayID"))
    await channel.purge(limit=50)
    await show_info_for_live_matches(channel)
    await show_info_for_upcomming_matches(channel)
    return True
