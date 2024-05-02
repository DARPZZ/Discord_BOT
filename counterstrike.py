import requests
import datetime
import aiohttp
from share import *
from bs4 import BeautifulSoup
import locale
 

from selenium import webdriver

async def scrape_matches_cs():
    url = "https://bo3.gg/matches/current"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()
    soup = BeautifulSoup(text, 'html.parser')
    mydate_time = datetime.datetime.now()
    mydate = mydate_time.date()
    mydate_string = str(mydate)
    matches = soup.find_all('div', class_='table-cell match')
    for match in matches:
        date = match.get('date')
        teamnames = match.find_all('div', class_='team-name')
        ko= str(date)
        hest = ko[0:10]
        hund = ko[11:16]
        if  teamnames:
            if mydate_string == hest:
                firstteam = teamnames[0].text.strip()
                secondteam = teamnames[1].text.strip()
                print(f"Team : {firstteam}   VS    Team : {secondteam}        time: {hund} ")
            
asyncio.run(scrape_matches_cs())