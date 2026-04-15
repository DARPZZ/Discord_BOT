from src.Games.steam_free_games_api import get_data
from share import *
class steam_free_games:
    def __init__(self,settings):
        self.embedVar = discord.Embed(color=0x00ff00)
        self.settings = settings
        epic_games_settings = self.settings("freeGames")
        self.channel = client.get_channel(epic_games_settings['freeGamesID'])

    async def getFreeGames(self):
        await self.channel.send(content="**Free games on Steam**")
        data = await get_data()
        if not data:
            await self.channel.send(content= "Could not find any free games")
            return
        for item in data:
            self.embedVar = discord.Embed(color=0x00ff00)
            title = item['title'].split('(Steam)')[0]
            original_price = item['worth']
            image = item['image']
            end_date = item['end_date']
            self.embedVar.add_field(name="Title",value=title,inline=False)
            self.embedVar.add_field(name="Original price",value=original_price,inline=False)
            self.embedVar.set_image(url=image)
            self.embedVar.add_field(name="Offer end at ", value=end_date,inline=False)
            await self.channel.send(embed= self.embedVar)