import discord
from discord.ext import commands 
intents = discord.Intents.default()
client = commands.Bot(command_prefix="!", intents=intents)
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import os
import requests
import asyncio
import aiohttp
import locale
def split_message(lines, limit=2000):
    """Splits a list of lines into chunks each of size less than limit."""
    messages = []
    current_message = ""
    for line in lines:
        if len(current_message) + len(line) + 1 > limit: 
            messages.append(current_message)
            current_message = line
        else:
            current_message += "\n" + line
    messages.append(current_message) 
    return messages