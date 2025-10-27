import requests
from share import *
class twitch:
    def __init__(self,settings):
        self.settings = settings
        
    async def get_live_twitch_streamer(self):
        twitch_settings = self.settings("twitch")
        twitch_settings_id = twitch_settings.get("twitchID")
        twitch_streamers = twitch_settings.get("streamers")
        channel = client.get_channel(twitch_settings_id)
        await channel.purge()
        await channel.send("Streamers that are live")
        for x in twitch_streamers:
            contents = requests.get('https://www.twitch.tv/' +x).content.decode('utf-8')
            if 'isLiveBroadcast' in contents: 
                embedVar = discord.Embed( color=0x9D00FF, description=x)
                await channel.send(embed=embedVar)
                