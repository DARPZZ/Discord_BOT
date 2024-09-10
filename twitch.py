import requests
from share import *
live_streamers = []
async def get_live_twitch_streamer(streamers):
        
        contents = requests.get('https://www.twitch.tv/' +streamers).content.decode('utf-8')

        if 'isLiveBroadcast' in contents: 
            live_streamers.append(streamers)
        channel = client.get_channel(1283139724990480485)
        await channel.purge(limit=25)
        if live_streamers:
            matches_message = "\n".join( live_streamers)
            live_streamers.clear()
            await channel.send("**Live streamers:**")
            for part in split_message(matches_message.split("\n")):
                await channel.send(part)
        else:
            await channel.send("No matches for today.")

