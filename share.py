import discord
intents = discord.Intents.default()
client = discord.Client(intents=intents)
from dotenv import load_dotenv
import os