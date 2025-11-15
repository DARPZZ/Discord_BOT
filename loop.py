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
import src.sports.NFL.NFL as NFL
from src.get_settings import read_settings_file as settings
from src.Games.epic_games_free import epic_games
@tasks.loop(hours=24)
async def start_epic_games_loop():
    epic_games_obj = epic_games(settings)
    await epic_games_obj.get_free_games_on_epic_games()
@tasks.loop(hours=17)
async def start_football_premierleague_table():
    premiere_league_table_obj =premiere_league_table.premiere_league_table(settings)
    await premiere_league_table_obj.scrape_matches()
@tasks.loop(hours=1) 
async def start_football_loop():
    football_obj = Football.football(settings)
    has_matches = await football_obj.scrape_matches()
    if not has_matches:
        start_football_loop.change_interval(hours=3)
    else:
        start_football_loop.change_interval(hours=1)
    
@tasks.loop(hours=6)
async def start_valorant_loop():
    valorant_obj = valorant.valorant()
    await valorant_obj.show_info()
@tasks.loop(hours=12)
async def start_nfl_loop():
    nfl_obj = NFL.NFL(settings)
    await nfl_obj.scrape_nfl_mathces()

@tasks.loop(hours=1)
async def twitch_loop():
    twitch_obj = twitch.twitch(settings)
    await twitch_obj.get_live_twitch_streamer()

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
    f1_obj =F1.f1(settings)
    await f1_obj.scrape_matches()
    
@tasks.loop(hours=48)
async def start_f1_driver_team_loop():
    f1_driver_obj =F1.f1(settings)
    await f1_driver_obj.Driver_team_standing()
    
@tasks.loop(hours=62)
async def start_Ufc_loop():
    ufc_obj = ufc.ufc(settings)
    await ufc_obj.scrape_matches()
