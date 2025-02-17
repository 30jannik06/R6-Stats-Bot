import asyncio
import os
from siegeapi import Auth
from dotenv import load_dotenv

load_dotenv()

UBISOFT_EMAIL = os.getenv("UBISOFT_EMAIL")
UBISOFT_PASSW = os.getenv("UBIFOT_PASSW")

async def get_player_stats(player_name: str, platform: str):
    auth = Auth(UBISOFT_EMAIL, UBISOFT_PASSW)
    player = await auth.get_player(name=player_name, platform=platform)
    
    #Spieler-Infos Laden
    await player.load_persona()
    await player.load_playtime()
    await player.load_ranked_v2()
    await player.load_progress()
    
   # stats = {
   #     "Name": player.name,
   #     "Profile Pic": player.profile_pic_url,
   #     "Streamer Nickname": player.persona.nickname,
   #     "Nickname Enabled": player.persona.enabled,
   #     "Total Time Played (s)": player.total_time_played,
   #     "Total Time Played (h)": player.total_time_played_hours,
   #     "Level": player.level,
   #     "Ranked Points": player.ranked_profile.rank_points,
   #     "Rank": player.ranked_profile.rank,
   #     "Max Rank Points": player.ranked_profile.max_rank_points,
   #     "Max Rank": player.ranked_profile.max_rank,
   #     "XP": player.xp,
   #     "Total XP": player.total_xp,
   #     "XP to level up": player.xp_to_level_up,
   # }
 
    await auth.close()
    return player