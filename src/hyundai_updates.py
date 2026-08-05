from share import *
from src.get_settings import read_settings_file
from dataclasses import dataclass
@dataclass
class UpdateInfoModel:
    genNm: str
    swVer: list
    postDate: str
class hyundai_updater:
    def __init__(self):
        self.channel_id = read_settings_file("hyndaiUpdateID")
        self.channel = client.get_channel(self.channel_id)
        self.owner_id = "<@338758353054466048>"
        
    def get_update_info(self):
        url = "https://update.hyundai.com/s3/static/latInfo/O2ncbPG8dG0y2Z8SzMENL4u56wjzdXNnIkOD94Jgrw%3D.json"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                matches = response.json()
                
                return matches
            else:
                print('Error:', response.status_code)
                return None
        except requests.exceptions.RequestException as e:
            print('Error:', e)
            return None
    def extract_data(self):
        data = self.get_update_info()
        car_model = UpdateInfoModel(
            data["genNm"],
            data["swInfo"][0]["swVer"],
            data["swInfo"][0]["postDate"]
        )
        return car_model
    async def show_info_to_user(self):
        car_info = self.extract_data()

        if car_info is None:
            return

        async for message in self.channel.history(limit=1):
            if message.embeds:
                old_embed = message.embeds[0]

                for field in old_embed.fields:
                    if field.name == "Update time" and field.value == car_info.postDate:
                        return
                await message.delete()
      
        embed = discord.Embed(
            title=f"Hyundai update info! ",
            color=discord.Color.blue()
        )
        embed.set_image(url="https://update.hyundai.com/s3/upload/global/carimg/20260702/gbimpuj2jjn89pwh0sbv8of0.png")
        embed.add_field(
            name="Car name",
            value=car_info.genNm,
            inline=False
        )
        embed.add_field(
            name="Software version E",
            value=car_info.swVer[0],
            inline=False
        )
        embed.add_field(
            name="Software version PE",
            value=car_info.swVer[1],
            inline=False
        )
        embed.add_field(
            name="Update time",
            value=car_info.postDate,
            inline=False
        )
        
        await self.channel.send(embed=embed,content=self.owner_id)
            