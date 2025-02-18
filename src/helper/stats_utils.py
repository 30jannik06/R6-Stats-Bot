import os
from typing import Dict
from siegeapi import Auth, Player
from dotenv import load_dotenv

from helper.logging_utils import error

load_dotenv()

UBISOFT_EMAIL: str = os.getenv("UBISOFT_EMAIL")
UBISOFT_PASSW: str = os.getenv("UBISOFT_PASSW")

SEASON_NAMES: Dict[int, str] = {
    3: "Black Ice", 4: "Dust Line", 5: "Skull Rain", 6: "Red Crow",
    7: "Velvet Shell", 8: "Health", 9: "Blood Orchid", 10: "White Noise",
    11: "Chimera", 12: "Para Bellum", 13: "Grim Sky", 14: "Wind Bastion",
    15: "Burnt Horizon", 16: "Phantom Sight", 17: "Ember Rise", 18: "Shifting Tides",
    19: "Void Edge", 20: "Steel Wave", 21: "Shadow Legacy", 22: "Neon Dawn",
    23: "Crimson Heist", 24: "North Star", 25: "Crystal Guard", 26: "High Calibre",
    27: "Demon Veil", 28: "Vector Glare", 29: "Brutal Swarm", 30: "Solar Raid",
    31: "Commanding Force", 32: "Dread Factor", 33: "Heavy Mettle",
    34: "Operation Deadly Omen", 35: "Operation Twin Shells", 36: "Operation Collision Point"
}

async def get_player_stats_data(player_name: str, platform: str):
    """Holt die Spieler-Statistiken und gibt ein Dictionary mit allen relevanten Infos zurück."""
    
    if not UBISOFT_EMAIL or not UBISOFT_PASSW:
        raise ValueError("UBISOFT_EMAIL oder UBISOFT_PASSW ist nicht gesetzt.")
    
    auth: Auth = Auth(UBISOFT_EMAIL, UBISOFT_PASSW)
    try:
        player: Player = await auth.get_player(name=player_name, platform=platform)
    except Exception as e:
        await auth.close()
        return
    
    # Spieler-Infos Laden
    await player.load_persona()
    await player.load_playtime()
    await player.load_ranked_v2()
    await player.load_progress()

    nowRank: str = player.ranked_profile.rank
    rank_parts: list[str] = nowRank.split(" ")

    base_url: str = "https://static.stats.cc/siege/ranks/"

    if nowRank == "Unranked":
        rankImg: str = f"{base_url}unranked-large.png"
        rank_name: str = "Unranked"
        rank_number: str = "N/A"
    elif len(rank_parts) == 2:
        rank_name = rank_parts[0].lower()
        rank_number = rank_parts[1]
        rankImg = f"{base_url}{rank_name}-{rank_number}-large.png"
    elif nowRank == "Champions":  
        rank_name = "champion"
        rank_number = "star"
        rankImg = f"{base_url}{rank_name}-{rank_number}-large.png"
    else:
        rank_name = nowRank  
        rank_number = "N/A"
        rankImg = f"{base_url}{rank_name}-large.png"

    maxRank: str = player.ranked_profile.max_rank
    name: str = player.name
    level: str = player.level
    profilePic: str = player.profile_pic_url_500
    platform: str = player._platform
    nowRP: str = player.ranked_profile.rank_points
    maxRP: str = player.ranked_profile.max_rank_points

    # Ranked Kills & Tode (Seasonal Stats)
    rankedKills: int = player.ranked_profile.kills
    rankedDeaths: int = player.ranked_profile.deaths
    seasonalKd: float = rankedKills / rankedDeaths if rankedDeaths > 0 else 0.0

    rankedWins: int = player.ranked_profile.wins
    rankedLosses: int = player.ranked_profile.losses
    seasonalWl: float = (rankedWins / (rankedWins + rankedLosses)) * 100 if (rankedWins + rankedLosses) > 0 else 0.0

    seasonName = SEASON_NAMES.get(player.ranked_profile.season_id, "Unknown Season")
    year: str = player.ranked_profile.season_code

    await auth.close()

    return {
        "name": name, "level": level, "profilePic": profilePic, "platform": platform,
        "nowRank": nowRank, "maxRank": maxRank, "nowRP": nowRP, "maxRP": maxRP,
        "rank_name": rank_name, "rank_number": rank_number, "rankImg": rankImg,
        "rankedKills": rankedKills, "rankedDeaths": rankedDeaths, "seasonalKd": round(seasonalKd, 2),
        "rankedWins": rankedWins, "rankedLosses": rankedLosses, "seasonalWl": round(seasonalWl, 0),
        "seasonName": seasonName, "year": year
    }