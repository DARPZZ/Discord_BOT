
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
            for x in elements:
                title = x.get("title")
                promo = x.get("promotions")
                offerType = x.get("offerType")
                img = x.get("keyImages")[0].get("url")
                if promo == None:
                    continue
                if(promo.get("promotionalOffers") != []):
                    await self.get_this_week_offeres(promo,title,offerType,img)
                    
                else:
                    await self.get_next_week_offers(promo,title,offerType,img)
                
    async def get_this_week_offeres(self,promo,title,offerType,img):
        promotionalOffers = promo.get("promotionalOffers")
        for promoffers in promotionalOffers:
            promotionalOffers2 = promoffers.get("promotionalOffers")
            for x in promotionalOffers2:
                discountSetting = x.get("discountSetting")
                discountPercentage = discountSetting.get("discountPercentage")
                if(discountPercentage != 0):
                    continue
                start_date = x.get("startDate")
                end_date = x.get("endDate")
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
                    "**Live Games**",
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
        
    async def get_next_week_offers(self,promo,title,offerType,img):
        upcomingPromotionalOffers = promo.get("upcomingPromotionalOffers")
        for x in upcomingPromotionalOffers:
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
                    "**Upcomming Games**",
                    img
                )

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