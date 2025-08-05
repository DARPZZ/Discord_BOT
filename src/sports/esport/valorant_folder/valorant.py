import src.sports.esport.pro_counterstrike_valorant_api_calls as api_call
import src.sports.esport.pro_esport as pro_esport
import src.sports.esport.counterstrike.create_counter_strike_embeds as  create_counter_strike_embeds
from src.get_settings import read_settings_file as settings
APIID =2
tournament_dict = {}
from share import *

async def show_info_for_upcomming_matches(channel):
    try:
        data = await api_call.get_counter_strike_valorant_pro_info_upcomming(APIID)
        if data:
            match_data = data['data']['tiers']['high_tier']['matches']
            for element in match_data:
                tournament_info = await pro_esport.place_tournament_info(element, data,tournament_dict)
                embedVar = discord.Embed(color=0xFF9DFF, title=f"{pro_esport.get_start_date(element)}")
                team_name = pro_esport.get_team_names(element)
                odds = pro_esport.get_odds(element)
                bo_type = element.get('bo_type')
                slug = element.get('slug')
                create_counter_strike_embeds.create_upcomming_matches_enmed(
                    embedVar, team_name, odds, bo_type, tournament_info[0], tournament_info[1]
                )
                streams = await pro_esport.get_stream_coverage(slug, api_call)
                await create_counter_strike_embeds.create_streams_embed(streams, embedVar)
                await channel.send(embed=embedVar)
    except Exception as e:
        print(f"Error in show_info_for_upcomming_matches: {e}")
        await channel.send("We could not find any high tier matches")

async def show_info():
    channel = client.get_channel(settings("proPlayIDValorant"))
    await channel.purge(limit=50)
    await show_info_for_upcomming_matches(channel)
