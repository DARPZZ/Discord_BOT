from share import *
async def scrape_team_standing(f1StartUrl, add_feilds):
    channel = client.get_channel(1381729288340111551)
    await channel.purge()
    url = f"{f1StartUrl}/standings"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()
            
    soup = BeautifulSoup(text, 'html.parser')
    table = soup.find_all('table', class_='standing-table__table')
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