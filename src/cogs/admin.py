import datetime

import discord
from discord.ext import commands
from discord import File

from colorama import Fore
from helper.logging_utils import *
from helper.stats_utils import get_player_stats

from dotenv import load_dotenv

load_dotenv()

class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong!')
    
    
    @discord.app_commands.command(name="stats", description="Remove User from Ticket")
    async def stats(self, interaction: discord.Interaction, player_name: str):
        stats = await get_player_stats(player_name)
        #print(stats)
        
        #profilePic: str = stats["Profile Pic"]
        nowRank: str = stats.ranked_profile.rank
        rank_parts = nowRank.split(" ")
        
        base_url = "https://static.stats.cc/siege/ranks/"
        
        if nowRank == "Unranked":
            rankImg = f"{base_url}unranked-large.png"
            rank_name = "Unranked"
            rank_number = "N/A"
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
            
        
        maxRank: str = stats.ranked_profile.max_rank
        name: str = stats.name
        level: str = stats.level
        platform: str = stats._platform
        nowRP: str = stats.ranked_profile.rank_points
        maxRP: str = stats.ranked_profile.max_rank_points
        
        rankedKills: int = stats.ranked_profile.kills
        rankedDeaths: int = stats.ranked_profile.deaths
        seasonalKd: float = rankedKills / rankedDeaths
        
        rankedWins: int = stats.ranked_profile.wins
        rankedLosses: int = stats.ranked_profile.losses
        seasonalWl: float = (rankedWins / (rankedWins + rankedLosses)) * 100
        bans: str = "none"
        seasonName: str = stats.ranked_profile.season_id
        year: str = stats.ranked_profile.season_code
        
        statsEmbed: discord.Embed = discord.Embed(description=f'Player information: **{name}**')
        statsEmbed.set_author(icon_url=stats.profile_pic_url, name=f'{name}')
        statsEmbed.set_thumbnail(url=rankImg)
        
        statsEmbed.add_field(name="General:", value=f'Level: **{level}**\n{platform}')
        statsEmbed.add_field(name="RP:", value=f'**{nowRP}**\nMax **{maxRP}**')
        statsEmbed.add_field(name="Rank:", value=f'**{nowRank}**\nMax **{maxRank}**')
        statsEmbed.add_field(name="Seasonal KD:", value=f'**{seasonalKd.__round__(2)}**\nKills **{rankedKills}**\nDeaths **{rankedDeaths}**')
        statsEmbed.add_field(name="Seasonal WL:", value=f'**{seasonalWl.__round__(0)}%**\nWins **{rankedWins}**\nLosses **{rankedLosses}**')
        statsEmbed.add_field(name="Game Bans:", value=f'{bans}')
        
        statsEmbed.set_footer(text=f'{seasonName} • {year}')
        statsEmbed.timestamp = datetime.datetime.now(datetime.timezone.utc)
                
        await interaction.response.send_message(embed=statsEmbed)
    
async def setup(client):
    await client.add_cog(Admin(client))
    command(f'🛠️ Loaded Admin Slash Commands')
