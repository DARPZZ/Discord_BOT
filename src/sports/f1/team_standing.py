from share import *
from src.helpers.connection import connection
class team_standing:
    def __init__(self):
        self.connection = connection(aiohttp,BeautifulSoup)
        
    async def scrape_team_standing(self,f1StartUrl,add_feilds,channelID):
        channel = client.get_channel(channelID)
        await channel.purge()
        url = f"{f1StartUrl}/standings"
        data  = await self.connection.create_connection(url)
        table = data.find_all('table', class_='standing-table__table')
        if table:
            team_table = table[1]
            standing_table__row = team_table.find_all('tr', class_='standing-table__row')
            for element in standing_table__row:
                embedVar = discord.Embed( color=0x9D00FF)
                team_name = element.find('td', class_='standing-table__cell standing-table__cell--name')
                if team_name != None:
                    team_points = team_name.findNextSibling()
                    team_name_text = team_name.text.strip()
                    team_points_text = team_points.text.strip()
                    add_feilds(embedVar,"Name: ", team_name_text)
                    add_feilds(embedVar,"Points: ", team_points_text)
                    await channel.send(embed=embedVar)