from share import *
from src.get_settings import read_settings_file as settings

async def get_logs():
    channel = client.get_channel(settings("logsID"))
    if channel is not None:
        try:
            with open("discord.log", "rb") as file:
                await channel.send("Here's the latest log file:", file=discord.File(file, "discord.log"))
        except FileNotFoundError:
            print("discord.log file not found.")
    else:
        print("Channel not found.")
    
    await client.close()
    