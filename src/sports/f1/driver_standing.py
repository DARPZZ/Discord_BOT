from share import *
from src.helpers.connection import connection
class driver_standing:
    def __init__(self):
        self.connection = connection(aiohttp,BeautifulSoup)
    async def scrape_driver_standing(self,f1StartUrl,add_feilds,channelID):
        url = f"{f1StartUrl}/standings"
        channel = client.get_channel(channelID)
        await channel.purge(limit=25)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                text = await response.text()
        soup = BeautifulSoup(text, 'html.parser')
        table = soup.find('table', class_='standing-table__table')
        table = soup.fi
        if table:
            rows = table.find_all('tr')[1:]
            for row in rows:
                embedVar = discord.Embed( color=0x9D00FF)
                cells = row.find_all('td')
                name = cells[1].text.strip()
                country = cells[2].text.strip()  
                team = cells[3].text.strip()     
                points = cells[4].text.strip()  
                add_feilds(embedVar,"Driver name: ", name)
                add_feilds(embedVar,"Country: ", country)
                add_feilds(embedVar,"Team: ", team)
                add_feilds(embedVar,"Points: ", points)
                await channel.send(embed=embedVar)
        