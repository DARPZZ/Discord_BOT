import requests
from share import *
live_streamers = []
async def get_live_twitch_streamer(streamers):
    channel = client.get_channel(1283139724990480485)
    await channel.purge()
    await channel.send("Streamers that are live")
    for x in streamers:
        contents = requests.get('https://www.twitch.tv/' +x).content.decode('utf-8')

        if 'isLiveBroadcast' in contents: 
            live_streamers.append(streamers)
            embedVar = discord.Embed( color=0x9D00FF, description=x)
            await channel.send(embed=embedVar)
            