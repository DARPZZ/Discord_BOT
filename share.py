import discord
from discord.ext import commands 
intents = discord.Intents.default()
client = commands.Bot(command_prefix="!", intents=intents)
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import os
import requests
import asyncio


    