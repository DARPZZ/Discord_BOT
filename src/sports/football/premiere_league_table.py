from share import *
import src.helpers.connection as connection

from enum import Enum
class international_football(Enum):
    champions_league = "Champions League"
    Europa_League = "Europa League"
    Nedrykning = "Nedrykning"
    
class premiere_league_table:
    def __init__(self,settings):
        self.settings = settings
        self.url = "https://www.livescore.dk/premier-league/stilling/"
        self.connection = connection.connection(aiohttp,BeautifulSoup)
    def add_space(self,number_of_space):
        space = "\u2003" * number_of_space
        return space

    def add_feilds_to_embed(self,x,embedvar):
        team_name = x.find('a')['title']
        status = x.find_all('td',class_='text-center')
        matches_played = self.strip_text(status[1])
        matches_won = self.strip_text( status[2])
        matches_drawn = self.strip_text( status[3])
        matches_lost = self.strip_text (status[4])
        goals = self.strip_text (status[5])
        team_points = self.strip_text( status[6])
        embedvar.add_field(
            name="", value=f"**{team_name} {team_points}**\n Matches played: {matches_played}{self.add_space(1)}Matches won: {matches_won} {self.add_space(1)} Matches drawn: {matches_drawn} {self.add_space(1)} Matches lost: {matches_lost} \n Goals: {goals}", inline=False
            )
        
    def strip_text(self,text_to_strip):
        return text_to_strip.text.strip()
    
    def decide_embed_color(self,x):
        if x.has_attr("title"):
            attribute = x['title']
            if attribute == international_football.champions_league.value:
                embedVar = discord.Embed( color=0x00ff00)
            elif attribute == international_football.Europa_League.value: 
                embedVar = discord.Embed( color=0x0000ff)
            elif attribute == international_football.Nedrykning.value:
                embedVar = discord.Embed( color=0xff0000)
        else:
            embedVar = discord.Embed(color=0xFFFFFF)
        return embedVar
    
    async def scrape_matches(self):
        football_settings = self.settings("football")
        channel = client.get_channel(football_settings["footballl_premiere_league_table"])
        await channel.purge()
        data = await self.connection.create_connection(url= self.url)
        start_element = data.find('table', class_="generic-table")
        nextt = start_element.find('tbody')
        nextt_childs = nextt.find_all('tr')
        for x in nextt_childs:
            embed = self.decide_embed_color(x)
            self.add_feilds_to_embed(x,embed)
            await channel.send(embed=embed)