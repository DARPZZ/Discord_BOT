
import datetime
from share import *
from src.Games.epic_games_api import get_data
class epic_games:
    def __init__(self,settings):
        self.settings = settings
        self.channel = client.get_channel(self.settings("epic_games"))
    def convert_date(self,date):
        clean_date = date.rstrip('Z') 
        dt = datetime.datetime.fromisoformat(clean_date)
        converted_date = dt.strftime("%d - %m")
        return converted_date
    
   
        
    async def check_promo_data(self,elements):
        LIVE_GAMES = "promotionalOffers"
        LIVE_GAMES_TEXT = "**Live Games**"
        UPCOMMING_GAMES ="upcomingPromotionalOffers"
        UPCOMMING_GAMES_TEXT = "**Upcomming Games**"
        for x in elements:
            title = x.get("title")
            promo = x.get("promotions")
            offerType = x.get("offerType")
            img = x.get("keyImages")[0].get("url")
            if promo == None:
                continue
            if(promo.get("promotionalOffers") != []):
                await self.offers(promo,title,offerType,img,LIVE_GAMES,LIVE_GAMES_TEXT)
            else:
                await self.offers(promo,title,offerType,img,UPCOMMING_GAMES,UPCOMMING_GAMES_TEXT)
   
    async def offers(self,promo,title,offerType,img,version,embed_title):
        PromotionalOffers = promo.get(version)
        for x in PromotionalOffers:
            promotionalOffers = x.get("promotionalOffers")
            for offers  in promotionalOffers:
                discountSetting = offers.get("discountSetting")
                discountPercentage = discountSetting.get("discountPercentage")
                if(discountPercentage != 0):
                    continue
                start_date = offers.get("startDate")
                end_date = offers.get("endDate")
                converted_start_date= self.convert_date(start_date)
                converted_end_date = self.convert_date(end_date)
                title = title
                offerType = offerType
                img = img
                await self.create_discord_embed(
                    title,
                    converted_start_date,
                    converted_end_date,
                    offerType,
                    embed_title,
                    img
                )
    async def create_discord_embed(self,title,start_date_converted,end_date_converted,offertype,type,img_url):
        embedVar_test = discord.Embed( color=0x9D00FF)
        embedVar_test.title = type
        embedVar_test.add_field(name="**Spil navn: **",value=title,inline=False)
        embedVar_test.add_field(name="**Start dato:** ",value=start_date_converted,inline=False)
        embedVar_test.add_field(name="**Slut Dato:** ",value=end_date_converted,inline=False)
        embedVar_test.add_field(name="**offertype:** ",value=offertype,inline=False)
        embedVar_test.set_image(url=img_url)
        await self.channel.send(embed=embedVar_test)
        

    async def get_free_games_on_epic_games(self):
        data = await get_data()
        await self.channel.purge()
        if not data:
            return
        elements = (
            data.get("data", {})
                .get("Catalog", {})
                .get("searchStore", {})
                .get("elements", [])
        )
        await self.check_promo_data(elements)