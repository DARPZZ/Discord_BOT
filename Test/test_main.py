import discord
import pytest
from datetime import datetime, timedelta
from src.sports.esport.pro_esport import get_start_date
from src.sports.esport.pro_esport import eror_message,get_team_names,get_odds
from bs4 import BeautifulSoup
import aiohttp
from unittest.mock import AsyncMock, MagicMock, patch
from src.Games.epic_games_free import epic_games
F1URL = "https://www.skysports.com/f1/schedule-results"
FOOTBALLURL ="https://www.livescore.dk/fodbold-i-tv/"
UFCURL = "https://www.ufc.com/events"
HEADLINE_CLASS = "c-card-event--result__headline"
DATE_CLASS = "c-card-event--result__date tz-change-data"
CONTAINER_CLASS = "l-listing__item views-row"

"""Test for Counter strike
"""
def test_valid_start_date():

    element = {'start_date': '2023-07-24T21:00:00.000000+0000'}
    expected = (datetime.strptime(element['start_date'], '%Y-%m-%dT%H:%M:%S.%f%z') + timedelta(hours=2)).strftime('%Y-%m-%d %H:%M')
    assert get_start_date(element) == expected

def test_missing_start_date():
    element = {} 
    assert get_start_date(element) == eror_message("start date")

def test_invalid_start_date_format():
    element = {'start_date': 'invalid-date-string'}
    assert get_start_date(element) == eror_message("start date")
@pytest.mark.asyncio
async def test_valid_cs_odds():
    element = {
        "bet_updates": {
            "team_1": {"coeff": 1.55},
            "team_2": {"coeff": 2.35}   
        }
    }
    result = await get_odds(element)
    assert result == "1.55 - 2.35"

@pytest.mark.asyncio
async def test_offers_filters_discount():
    def fake_settings(key):
        if key == "epicGames":
            return {"epicGamesID": 999999999999999999}
        return None

    eg = epic_games(settings=fake_settings)
    promo = {
        "promotionalOffers": [{
            "promotionalOffers": [{
                "discountSetting": {"discountPercentage": 50},
                "startDate": "2025-11-01T00:00:00Z",
                "endDate": "2025-11-08T00:00:00Z"
            }]
        }]
    }
    result = await eg.offers(promo, "Test Game", "BASE", "http://image.url", "promotionalOffers", "**Live Games**")
    assert result is None
    
@pytest.mark.asyncio
async def test_create_discord_embed_structure():
    def fake_settings(key):
        if key == "epicGames":
            return {"epicGamesID": 999999999999999999}
        return None

    eg = epic_games(settings=fake_settings)

    embed = await eg.create_discord_embed(
        "Test Game", "01 - 11", "08 - 11", "BASE", "**Live Games**", "http://image.url"
    )

    assert isinstance(embed, discord.Embed)
    assert embed.title == "**Live Games**"
    assert embed.fields[0].value == "Test Game"
    
@pytest.mark.asyncio
async def test_check_promo_data_populates_lists():
    def fake_settings(key):
        if key == "epicGames":
            return {"epicGamesID": 999999999999999999}
        return None

    eg = epic_games(settings=fake_settings)
    eg.offers = AsyncMock(return_value="EMBED")
    elements = [{
        "title": "Test Game",
        "promotions": {
            "promotionalOffers": [{}]
        },
        "offerType": "BASE",
        "keyImages": [{"url": "http://image.url"}]
    }]
    await eg.check_promo_data(elements)
    assert eg.live_embds_list == ["EMBED"]
    assert eg.upcomming_embds_list == []

"""
Test for F1

"""
@pytest.mark.asyncio
async def test_f1_html_structure():
    async with aiohttp.ClientSession() as session:
        async with session.get(F1URL) as response:
            assert response.status == 200, f"Failed to fetch page: {response.status}"
            html = await response.text()

    soup = BeautifulSoup(html, 'html.parser')

    races_all = soup.find('div', class_='f1-races')
    assert races_all is not None, "Missing 'div.f1-races'"

    races = races_all.find_all('a', class_='f1-races__race')
    assert races, "No '.f1-races__race' elements found"

    race = races[0]
    racename = race.find('h2', class_='f1-races__race-name')
    assert racename is not None, "Missing race name"

    tbody = race.find('tbody')
    assert tbody is not None, "Missing <tbody>"

    td = tbody.findChild()
    siblings = td.findNextSiblings()
    
    assert len(siblings) >= 2, "Expected at least 2 sibling <td> elements"
    
    
# """
# Test for football
# """
# @pytest.mark.asyncio
# async def test_livescore_html_structure():
#     try:
#         async with aiohttp.ClientSession() as session:
#             async with session.get(FOOTBALLURL) as response:
#                 assert response.status == 200, f"Failed to fetch page: {response.status}"
#                 html = await response.text()
#     except aiohttp.ClientError as e:
#         pytest.skip(f"Skipping test due to network error: {e}")
#         return

#     soup = BeautifulSoup(html, 'html.parser')

#     todays_matches = soup.find('div', class_='tv-table tv-table--football')
#     assert todays_matches is not None, "Missing 'div.tv-table tv-table--football'"


"""
Test UFC
"""
@pytest.mark.asyncio
async def test_ufc_html_structure():
    headers = {
        'accept-language': 'da-DK,da;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        'cookie': 'STYXKEY_region=WORLD.DK.en-zxx.Default'
    }

    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(UFCURL) as response:
                assert response.status == 200, f"Failed to fetch page: {response.status}"
                html = await response.text()
    except aiohttp.ClientError as e:
        pytest.skip(f"Skipping test due to network error: {e}")
        return

    soup = BeautifulSoup(html, 'html.parser')
    matches = soup.find_all('div', class_=CONTAINER_CLASS)
    assert matches, f"No matches found with class '{CONTAINER_CLASS}'"

    for match in matches[:3]:
        headline_tags = match.find_all('h3', class_=HEADLINE_CLASS)
        assert headline_tags, f"Missing headlines with class '{HEADLINE_CLASS}'"

        date_tags = match.find_all('div', class_=DATE_CLASS)
        assert date_tags, f"Missing date tags with class '{DATE_CLASS}'"

        fighters = headline_tags[0].text.strip()
        match_info = date_tags[0].text.strip().split(" ")

        assert len(match_info) >= 6, "Unexpected date format — fewer than expected parts"

        month = match_info[1].capitalize()
        day = match_info[2].strip(',')
        time = match_info[4]
        time_zone = match_info[5]

        assert month.isalpha(), f"Month value '{month}' seems wrong"
        assert day.isdigit(), f"Day value '{day}' is not numeric"
        assert time.count(":") == 1, f"Time '{time}' is not in HH:MM format"
        assert time_zone in ["ET","PM", "PT", "BST", "CEST", "UTC","AM"], f"Unexpected timezone: '{time_zone}'"