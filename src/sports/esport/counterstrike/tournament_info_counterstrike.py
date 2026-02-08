import  src.sports.esport.pro_counterstrike_valorant_api_calls as pro_counterstrike_valorant_api_calls
import requests
import asyncio
from datetime import datetime
from share import *
from src.get_settings import read_settings_file as settings

def get_current_date():
    return datetime.today().strftime('%Y-%m-%d')

def days_between(d1, d2):
    d1 = datetime.strptime(d1[:10], "%Y-%m-%d")
    d2 = datetime.strptime(d2[:10], "%Y-%m-%d")
    return abs((d2 - d1).days)

def get_attending_teams(element):
    names_array = []
    teams = element.get('teams')
    for team in teams:
        team_name = team.get('name')
        names_array.append(team_name)
    if names_array == []:
        names_array.append("We could not find the attending teams")
        return names_array
    return names_array

async def get_upcomming_tournaments():
    tournament_settings = settings("cs")
    channel = client.get_channel(tournament_settings['proPlaIDCsTournament'])
    await channel.purge(limit=50)
    data = await pro_counterstrike_valorant_api_calls.get_counter_strike_upcomming_tournaments()
    if data:
        results = data['results']
        for element in results:
            status = element.get('status')
            tier = element.get('tier')
            tier = tier.lower()
            if (tier == "s" or tier == "a"):
                name_of_tournament = element.get('name')
                if status == "current":
                    embedVar = discord.Embed(color=0x008000, title=f"{name_of_tournament}")
                    embedVar.add_field(name="", value= f"Has started")
                else:
                    start_date = element.get('start_date')
                    days_until_tournament = days_between(get_current_date(),start_date)
                    embedVar = discord.Embed(color=0xFFFF00, title=f"{name_of_tournament}")
                    embedVar.add_field(name="Starting in", value= f"{days_until_tournament} day(s)")
                logos = get_attending_teams(element)
                embedVar.add_field(name="", value="**Teams attending:**", inline=False)
                message  =""
                for x in logos:
                    logos_stripped = x.strip()
                    message = f"{message}{logos_stripped}\u2003 "
                embedVar.add_field (name="",value=f"{message}", inline=True)
                await channel.send(embed=embedVar)
    else:
        await channel.send("We could not find any information about upcomming tournaments")