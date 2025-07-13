import os
import json
import requests
import src.Sports.CounterStrike.GetPlayerInfo.steam_api_call as steamAPI
#import steam_api_call as steamAPI
import asyncio
import discord
import dotenv
from share import *
CS2_APP_ID = 730
    
def get_hs_procentage(data,kills,stats_list):
    stats = {s['name']: s['value'] for s in stats_list}
    total_kills_headshot = stats.get("total_kills_headshot")
    hs_procentage = (total_kills_headshot / kills) * 100
    return round(hs_procentage,2)

def calculate_map_win_procentage(stats_list):
    stats = {s['name']: s['value'] for s in stats_list}
    total_matches_played = stats.get("total_matches_played")
    total_matches_won = stats.get("total_matches_won")
    total_win_procentage = (total_matches_won / total_matches_played) * 100
   
    return round(total_win_procentage,2)

def calculate_kd(stats_list):

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
    if(playtime_data['response'] == {}):
        return
    games_list = playtime_data['response']['games']
    for game in games_list:
        app_id = game['appid']
        playtime_forever = game.get("playtime_forever")
        
        playtime_past_2_weeks = game.get('playtime_2weeks', 0)
        if(app_id == CS2_APP_ID):

            return [playtime_forever, playtime_past_2_weeks]
        
async def create_embed(kills,death,kd,wind,timeplayed,timeplayed_2_weeks,hs):
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

    embed.set_thumbnail(url="https://i.imgur.com/R66g1Pe.png")
    embed.set_footer(text="Stats generated")
    return embed

        
async def get_info(PlayerID):
    user_stats_data = await steamAPI.GetUserStatsForGame(PlayerID)
    user_playtime_data = await user_playtime(PlayerID)
    if(user_stats_data == None):
        embed = discord.Embed(
        title="🎮 Player Stats",
        description="performance overview",
        )
        
        embed.add_field(name="🔫 Profile is: ", value=f"Private", inline=False)
        return embed
    stats_list = user_stats_data['playerstats']['stats']
    kd_data = calculate_kd(stats_list)
    hs_pro = get_hs_procentage(stats_list,kd_data.get("kills"),stats_list)
    winprocentage = calculate_map_win_procentage(stats_list)
    total_playtime = user_playtime_data[0] / 60
    two_weeks_playtime = user_playtime_data[1] / 60
    two_weeks_playtime_round = round(two_weeks_playtime,2)
    total_playtime_round = round(total_playtime,2)
    kills = kd_data.get("kills")
    deaths = kd_data.get("deaths")
    kd = kd_data.get("kd")
    embed = await create_embed(kills,deaths,kd,winprocentage,total_playtime_round,two_weeks_playtime_round,hs_pro)
    return embed
    