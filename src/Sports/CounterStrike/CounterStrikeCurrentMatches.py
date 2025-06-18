from share import *

async def scrape_current_matches(channel,headers,url,show_rateing,get_team_names):
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            text = await response.text()
    soup = BeautifulSoup(text, 'html.parser')
    matches = soup.find_all('div', class_= 'c-matches-group-rows')
    for match in matches:
        table_rows = match.find_all('div', class_='table-row table-row--current')
        for table_row in table_rows:
            embedVar = discord.Embed( color=0x9D00FF, description="Live Match")
            if await show_rateing(table_row):
                #print(f"**Teams: ** {first_team} VS {second_team}\n**Score: **\n{'-'*60}\n")
                embedVar.add_field(name="**Teams: **",value= await get_team_names(table_row),inline=False)
                embedVar.add_field(name="**Time: **", value="Live", inline=False)
                await channel.send(embed=embedVar)