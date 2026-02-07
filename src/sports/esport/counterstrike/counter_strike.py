
import src.sports.esport.pro_counterstrike_valorant_api_calls as api_call
from share import *
import src.sports.esport.counterstrike.create_counter_strike_embeds as  create_counter_strike_embeds
import src.sports.esport.pro_esport as pro_esport
import datetime
from src.get_settings import read_settings_file as settings
APIID = 1
total_matches = []
tournament_dict = {}
ERROR_MESSAGE = "We could not find any high tier matches, that are upcomming or live"

async def show_info_for_upcomming_matches(channel):
    try:
        data = await api_call.get_counter_strike_valorant_pro_info_upcomming(APIID)
        if data:
            match_data = data['data']['tiers']['high_tier']['matches']
            if(match_data is None):
                return 
            for element in match_data:
                stars = element.get('stars')
                tournament_info_task = await pro_esport.place_tournament_info(element, data,tournament_dict)
                tournament_name,tournament_price = tournament_info_task
                if stars < 2 and "Major" not in tournament_name:
                    continue
                embedVar = discord.Embed(color=0xFF9DFF, title=f"{pro_esport.get_start_date(element)}")
                team_names_task = pro_esport.place_team_names_values(data,element)
                odds_task = pro_esport.get_odds(element)
                bo_type = element.get('bo_type')
                slug = element.get('slug')
                streams_task = pro_esport.get_stream_coverage(slug, api_call)
                streams,team_names,odds = await asyncio.gather(
                    streams_task,team_names_task,odds_task
                )
                create_counter_strike_embeds.create_upcomming_matches_enmed(
                    embedVar,team_names,odds,bo_type,tournament_name,tournament_price
                )
                total_matches.append(embedVar)
                await create_counter_strike_embeds.create_streams_embed(streams, embedVar)
                await channel.send(embed=embedVar)
    except Exception as e:
        print(f"Error in show_info_for_upcomming_matches: {e}")


async def show_info_for_live_matches(channel):
    try:
        data = await api_call.get_counter_strike_valorant_pro_info_live(APIID)
        if(data):
            match_data = data['data']
            if(match_data is None):
                return
            for element in match_data:
                tournament_info_task = await pro_esport.place_tournament_info(element,data,tournament_dict)
                tournament_name,tournament_price = tournament_info_task
                stars = element.get('stars',0)
                if stars < 2  and "Major" not in tournament_name:
                    continue
                maps = pro_esport.get_maps(element)
                embedVar = discord.Embed( color=0x9DFF00,title=f"**Live**")
                team_names = await pro_esport.place_team_names_values(data,element)
                team1_score = element.get('team1_score')
                team2_score =element.get('team2_score')
                create_counter_strike_embeds.create_live_matches_enmed(embedVar,team_names,team1_score,team2_score,tournament_name,tournament_price)
                embedVar.add_field(name=f"",value="**Maps: **",inline=False)
                maps =  pro_esport.get_maps(element)
                for mapp in maps:
                    embedVar.add_field(name=f"",value=mapp,inline=False)
                slug = element.get('slug')
                streams = await pro_esport.get_stream_coverage(slug,api_call)
                total_matches.append(embedVar)
                await create_counter_strike_embeds.create_streams_embed(streams,embedVar)
                await channel.send(embed=embedVar)
    except Exception as e:
        print(f"Error in show_info_for_live_matches: {e}")
        
async def translate_team_id_to_team_name(data):
   
    included = data['included']
    if (included != {}):
        team_data = included['teams']
    
        team_map = {team_id: info["name"] for team_id, info in team_data.items()}
        return team_map

def convert_time(start_date,end_date):
    start = datetime.datetime.fromisoformat(start_date)
    end = datetime.datetime.fromisoformat(end_date)
    start_time = start.strftime("%H:%M")
    start_date = start.strftime("%Y-%m-%d")
    end_time = end.strftime("%H:%M")
    end_date = end.strftime("%Y-%m-%d")
    return [start_date,start_time,end_date,end_time]

async def show_info_for_finished_matches():
    try:
        no_matches_today = "No matches has finsihed today"
        channel = client.get_channel(settings("finsihed_counterstrike_matches"))
        await channel.purge()
        data = await api_call.get_counter_strike_pro_info_finished()
        if(data):
            team_map = await translate_team_id_to_team_name(data=data)
            match_data = data['data']['tiers']['high_tier']['matches']
            if(match_data is None):
                return
            for match in match_data:
                embedVar = discord.Embed(color=0xFF9DFF)
                start_date = match['start_date']
                end_date = match['end_date']
                winner_team_id = match['winner_team_id']
                team1_id = match['team1_id']
                team2_id = match['team2_id']
                team1_score = match['team1_score']
                team2_score = match['team2_score']
                start_date_final,start_time_final,end_date_final,end_time_final = convert_time(start_date,end_date)
                create_counter_strike_embeds.crate_finsihed_matches_embed(
                    embedVar,
                    f"{team_map[str(team1_id)]} VS {team_map[str(team2_id)]}",
                    f"{team_map[str(winner_team_id)]}",
                    f"{team1_score} - {team2_score}",
                    f"{start_date_final} - {start_time_final}",
                    f"{end_date_final} - {end_time_final}"
                )
                await channel.send(embed=embedVar)
        else:
            await channel.send(no_matches_today)
    except Exception as ex:
        await channel.send(no_matches_today)            

async def show_info():
    channel = client.get_channel(settings("proPlayIDCs"))
    await channel.purge(limit=50)
    await show_info_for_live_matches(channel)
    await show_info_for_upcomming_matches(channel)
    if(len(total_matches) <= 0):
       embedVar = discord.Embed( color=0x9DFF00)
       embedVar.add_field(name="",value=ERROR_MESSAGE,inline=False)
       await channel.send(embed=embedVar)
    total_matches.clear()
    return True
