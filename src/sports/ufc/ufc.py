from share import *
from src.helpers.connection import connection
from src.helpers.feilds import feilds
class ufc:
    def __init__(self,settings):
        self.embedVar = discord.Embed( color=0x00ff00 )
        self.feilds_obj = feilds(self.embedVar)
        self.settings = settings
        self.url = "https://www.ufc.com/events"
        self.headers= {
            'accept-language': 'da-DK,da;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'max-age=0',
            'cookie': 'STYXKEY_region=WORLD.DK.en-zxx.Default'
        }
    def get_time_and_date(self,split_match_info):
        month = split_match_info[1].capitalize()
        day = split_match_info[2].strip(',')
        time = split_match_info[4]
        time_zone = split_match_info[5]
        time += time_zone
        mma_kamp_edt = f" {month} {day} {time}"
        return mma_kamp_edt
    
    async def scrape_matches(self):
        ufc_settings = self.settings('ufc')
        channel = client.get_channel(ufc_settings['ufcID'])
        await self.feilds_obj.clear_feilds(channel)
        connection_obj =connection(aiohttp,BeautifulSoup)
        data = await connection_obj.create_connection(url=self.url, headers= self.headers)
        matches = data.find_all('div', class_='l-listing__item views-row')
        for match in matches:
            self.embedVar.clear_fields()   
            head_line = match.find_all('h3', class_='c-card-event--result__headline')
            match_info = match.find_all('div', class_='c-card-event--result__date tz-change-data')
            fighters = head_line[0].text.strip()
            stripped_match_info = match_info[0].text.strip()
            split_match_info = stripped_match_info.split(" ")
            self.feilds_obj.generate_feilds("**Date and time:**",self.get_time_and_date(split_match_info))
            self.feilds_obj.generate_feilds("**Headline:**",fighters)
            await channel.send(embed=self.embedVar)
