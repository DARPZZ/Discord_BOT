
import src.sports.esport.pro_counterstrike_valorant_api_calls as api_call
from share import *
import src.sports.esport.counterstrike.create_counter_strike_embeds as  create_counter_strike_embeds
import src.sports.esport.pro_esport as pro_esport
from src.get_settings import read_settings_file as settings
APIID = 1
tournament_dict = {}
ERROR_UPCOMMING_MATCHES = "We could not find any high tier matches, that are upcomming"
ERROR_LIVE_MATCHES = "We could not find any high tier matches, that are live"
async def show_info_for_upcomming_matches(channel):
    try:
        data = await api_call.get_counter_strike_valorant_pro_info_upcomming(APIID)
        if data:
            match_data = data['data']['tiers']['high_tier']['matches']
            if(match_data is None):
                await channel.send(ERROR_UPCOMMING_MATCHES)
                return 
            for element in match_data:
                stars = element.get('stars')
                if stars < 2:
                    continue
                tournament_info_task =  pro_esport.place_tournament_info(element, data,tournament_dict)
                embedVar = discord.Embed(color=0xFF9DFF, title=f"{pro_esport.get_start_date(element)}")
                team_names_task = pro_esport.place_team_names_values(data,element)
                odds_task = pro_esport.get_odds(element)
                bo_type = element.get('bo_type')
                slug = element.get('slug')
                streams_task = pro_esport.get_stream_coverage(slug, api_call)
                tournament_info, streams,team_names,odds = await asyncio.gather(
                    tournament_info_task, streams_task,team_names_task,odds_task
                )
                create_counter_strike_embeds.create_upcomming_matches_enmed(
                    embedVar, team_names, odds, bo_type, tournament_info[0], tournament_info[1]
                )
                
                await create_counter_strike_embeds.create_streams_embed(streams, embedVar)
                await channel.send(embed=embedVar)
    except Exception as e:
        print(f"Error in show_info_for_upcomming_matches: {e}")
        await channel.send(ERROR_UPCOMMING_MATCHES)


async def show_info_for_live_matches(channel):
    try:
        data = await api_call.get_counter_strike_valorant_pro_info_live(APIID)
        if(data):
            match_data = data['data']
            if(match_data is None):
                await channel.send(ERROR_UPCOMMING_MATCHES) 
            for element in match_data:
                stars = element.get('stars',0)
                if (stars < 2):
                    continue
                maps = pro_esport.get_maps(element)
                tournament_info = await pro_esport.place_tournament_info(element,data,tournament_dict)
                embedVar = discord.Embed( color=0x9DFF00,title=f"**Live**")
                team_names = await pro_esport.place_team_names_values(data,element)
                team1_score = element.get('team1_score')
                team2_score =element.get('team2_score')
                create_counter_strike_embeds.create_live_matches_enmed(embedVar,team_names,team1_score,team2_score,tournament_info[0],tournament_info[1])
                
                embedVar.add_field(name=f"",value="**Maps: **",inline=False)
                maps =  pro_esport.get_maps(element)
                for mapp in maps:
                    embedVar.add_field(name=f"",value=mapp,inline=False)
                slug = element.get('slug')
                streams = await pro_esport.get_stream_coverage(slug,api_call)
                await create_counter_strike_embeds.create_streams_embed(streams,embedVar)
                await channel.send(embed=embedVar)
    except Exception as e:
        print(f"Error in show_info_for_live_matches: {e}")
        await channel.send(ERROR_LIVE_MATCHES)        

async def show_info():
    
    channel = client.get_channel(settings("proPlayIDCs"))
    await channel.purge(limit=50)
    await show_info_for_live_matches(channel)
    await show_info_for_upcomming_matches(channel)
    return True
