from share import *
from discord.ext import tasks
import src.sports.football.football as Football
import src.sports.esport.counterstrike.counter_strike as counter_strike
import src.sports.esport.valorant_folder.valorant as valorant
import src.sports.ufc.ufc as ufc
import src.sports.f1.f1 as F1
import src.twitch.twitch as twitch
import src.sports.esport.counterstrike.tournament_info_counterstrike as counter_strike_tournament
import src.sports.football.premiere_league_table as premiere_league_table
@tasks.loop(hours=17)
async def start_football_premierleague_table():
    await premiere_league_table.scrape_matches()
@tasks.loop(hours=1) 
async def start_football_loop():
    has_matches = await Football.scrape_matches()
    if not has_matches:
        start_football_loop.change_interval(hours=3)
    else:
        start_football_loop.change_interval(hours=1)
        
@tasks.loop(hours=6)
async def start_valorant_loop():
    await valorant.show_info()

@tasks.loop(hours=1)
async def twitch_loop():
    await twitch.get_live_twitch_streamer()

@tasks.loop(minutes=20)
async def start_counterstrike_loop():
    has_matches = await counter_strike.show_info()
    if not has_matches:
         start_counterstrike_loop.change_interval(minutes=20)
    else:
         start_counterstrike_loop.change_interval(minutes=20)
         
@tasks.loop(hours=24)
async def start_counterstrike_tournament_loop():
    await counter_strike_tournament.get_upcomming_tournaments()
        
@tasks.loop(hours=48)
async def start_f1_loop():
    await F1.scrape_matches()
    
@tasks.loop(hours=48)
async def start_f1_driver_team_loop():
    await F1.Driver_team_standing()
    
@tasks.loop(hours=48)
async def start_Ufc_loop():
    await ufc.scrape_matches()
