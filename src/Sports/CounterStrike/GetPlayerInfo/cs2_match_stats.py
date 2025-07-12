import os
import json
import requests
import src.Sports.CounterStrike.GetPlayerInfo.steam_api_call as steamAPI
import asyncio
import dotenv
from share import *
CS2_APP_ID = 730
    
def get_hs_procentage(data,kills):
    stats_list = data['playerstats']['stats']
    stats = {s['name']: s['value'] for s in stats_list}
    total_kills_headshot = stats.get("total_kills_headshot")
    hs_procentage = (total_kills_headshot / kills) * 100
    return round(hs_procentage,2)

def calculate_map_win_procentage(data):
    stats_list = data['playerstats']['stats']
    stats = {s['name']: s['value'] for s in stats_list}
    total_matches_played = stats.get("total_matches_played")
    total_matches_won = stats.get("total_matches_won")
    total_win_procentage = (total_matches_won / total_matches_played) * 100
   
    return round(total_win_procentage,2)

def calculate_kd(data):
    stats_list = data['playerstats']['stats']
    stats = {s['name']: s['value'] for s in stats_list}
    kills = stats.get('total_kills')
    death = stats.get('total_deaths')
    kd = kills /death
    kd_rounded = round(kd,2)
    kd_dict = {
        "kills": kills,
        "deaths": death,
        "kd": kd_rounded
    }
    return kd_dict

async def user_playtime(PlayerID):
    playtime_data = await steamAPI.GetPlaytime(PlayerID)
    games_list = playtime_data['response']['games']
    for game in games_list:
        app_id = game['appid']
        playtime_forever = game.get("playtime_forever")
        
        playtime_past_2_weeks = game.get('playtime_2weeks', 0)
        if(app_id == CS2_APP_ID):

            return [playtime_forever, playtime_past_2_weeks]

async def create_embed(kills,death,kd,wind,timeplayed,timeplayed_2_weeks,hs):
    
    channel = client.get_channel(1235813854580179125)
    embed = discord.Embed(
        title="🎮 Player Stats",
        description="performance overview",
    )

    
    embed.add_field(name="🔫 Total Kills", value=f"{kills:,}", inline=True)
    embed.add_field(name="💀 Total Deaths", value=f"{death:,}", inline=True)
    embed.add_field(name="⚖️ K/D Ratio", value=str(kd), inline=True)
    embed.add_field(name="🏆 Win Percentage", value=f"{wind}%", inline=True)
    embed.add_field(name="⏱️ Time Played (2 Weeks)", value=timeplayed_2_weeks, inline=True)
    embed.add_field(name="📅 Time Played (All Time)", value=timeplayed, inline=True)
    embed.add_field(name="🔫 Headshot %", value=hs, inline=True)

    # Optional: add thumbnail (game logo or avatar)
    embed.set_thumbnail(url="https://i.imgur.com/R66g1Pe.png")  # Example image
    embed.set_footer(text="Stats generated")
    return embed

        
async def get_info(PlayerID):
    user_stats_data = await steamAPI.GetUserStatsForGame(PlayerID)
    user_playtime_data = await user_playtime(PlayerID)
    kd_data = calculate_kd(user_stats_data)
    hs_pro = get_hs_procentage(user_stats_data,kd_data.get("kills"))
    winprocentage = calculate_map_win_procentage(user_stats_data)
    total_playtime = user_playtime_data[0] / 60
    two_weeks_playtime = user_playtime_data[1] / 60
    two_weeks_playtime_round = round(two_weeks_playtime,2)
    total_playtime_round = round(total_playtime,2)
    kills = kd_data.get("kills")
    deaths = kd_data.get("deaths")
    kd = kd_data.get("kd")
    embed = await create_embed(kills,deaths,kd,winprocentage,total_playtime_round,two_weeks_playtime_round,hs_pro)
    return embed
    