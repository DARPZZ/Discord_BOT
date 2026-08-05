from unittest.mock import AsyncMock, patch

import pytest

from src.sports.esport import pro_esport


@pytest.mark.parametrize(
    ("element", "expected"),
    [
        ({}, ["We could not get any map data for this match"]),
        (
            {
                "games": [
                    {"map_name": "Dust 2", "status": "finished"},
                    {"status": "upcoming"},
                ]
            },
            [
                "Map name: Dust 2 - Map status: finished",
                "Map name: Unknown - Map status: upcoming",
            ],
        ),
    ],
)
def test_get_maps(element, expected):
    assert pro_esport.get_maps(element) == expected


def test_get_team_names():
    pro_esport.team_name_dict.clear()
    data = {
        "included": {
            "teams": {
                "1": {"name": "Astralis"},
                "2": {"name": "Vitality"},
            }
        }
    }

    assert pro_esport.get_team_names(data) == {
        "1": "Astralis",
        "2": "Vitality",
    }
    assert pro_esport.get_team_names({}) is None


@pytest.mark.asyncio
async def test_place_team_names_values():
    data = {
        "included": {
            "teams": {
                "1": {"name": "Astralis"},
                "2": {"name": "Vitality"},
            }
        }
    }

    result = await pro_esport.place_team_names_values(
        data, {"team1_id": 1, "team2_id": 2}
    )
    assert result == "Astralis VS Vitality"

    with patch.object(pro_esport, "get_team_names", return_value=None):
        result = await pro_esport.place_team_names_values({}, {})
    assert result == "Could not find the team names"


@pytest.mark.asyncio
async def test_tournament_info():
    data = {
        "included": {
            "tournaments": {
                "ignored-key": {
                    "id": 7,
                    "name": "Major",
                    "prize": 1_250_000,
                }
            }
        }
    }
    tournaments = {99: {"old": "value"}}

    await pro_esport.get_tournament_info(data, tournaments)
    assert tournaments == {
        7: {
            "tournament_name": "Major",
            "tournament_prize_pool": 1_250_000,
        }
    }

    result = await pro_esport.place_tournament_info(
        {"tournament": "7"}, data, tournaments
    )
    assert result == ["Major", "1.250.000"]

    result = await pro_esport.place_tournament_info({}, data, tournaments)
    assert result is None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("element", "expected"),
    [
        ({}, None),
        ({"bet_updates": {"team_1": None}}, "Unable to get data for odds"),
    ],
)
async def test_get_odds_missing_or_invalid(element, expected):
    assert await pro_esport.get_odds(element) == expected


@pytest.mark.asyncio
async def test_get_stream_coverage_filters_and_limits_streams():
    streams = [
        {"raw_url": "https://dk", "language": "da", "viewers_number": 5},
        *[
            {
                "raw_url": f"https://stream-{number}",
                "language": "en",
                "viewers_number": number,
            }
            for number in range(7)
        ],
    ]
    api = AsyncMock()
    api.get_counter_strike_valorant_stream_coverage.return_value = {
        "streams": streams
    }

    result = await pro_esport.get_stream_coverage("match-slug", api)

    assert len(result) == 6
    assert "https://dk" not in result
    api.get_counter_strike_valorant_stream_coverage.assert_awaited_once_with(
        "match-slug"
    )


@pytest.mark.asyncio
async def test_get_stream_coverage_handles_api_errors():
    api = AsyncMock()
    api.get_counter_strike_valorant_stream_coverage.side_effect = RuntimeError(
        "API unavailable"
    )

    assert await pro_esport.get_stream_coverage("match-slug", api) == {}
