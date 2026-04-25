from src.Games.free_games_api import get_data
from share import *
class free_games:
    def __init__(self,settings):
        self.embedVar = discord.Embed(color=0x00ff00)
        self.settings = settings
        epic_games_settings = self.settings("freeGames")
        self.channel = client.get_channel(epic_games_settings['freeGamesID'])
        
    async def get_free_games_platform(self,platform,platform_text):
        await self.channel.send(content=f"**Free games on {platform_text}**")
        data = await get_data(platform)
        if not data:
            await self.channel.send(content= f"Could not find any free games for {platform}")
            return
        for item in data:
            self.embedVar = discord.Embed(color=0x00ff00)
            if (platform =="steam"):
                title = item['title'].split('(Steam)')[0]
            elif (platform =="epic-games-store"):
                title = item['title'].split('(Epic Games)')[0]
            original_price = item['worth']
            image = item['image']
            end_date = item['end_date']
            self.embedVar.add_field(name="Title",value=title,inline=False)
            self.embedVar.add_field(name="Original price",value=original_price,inline=False)
            self.embedVar.set_image(url=image)
            self.embedVar.add_field(name="Offer end at ", value=end_date,inline=False)
            await self.channel.send(embed= self.embedVar)
            
    async def get_free_games(self):
        await self.channel.purge()
        platforms = [
            ("steam", "Steam"),
            ("epic-games-store", "Epic Games")
        ]
        for platform, platform_text in platforms:
            await self.get_free_games_platform(platform=platform, platform_text=platform_text)