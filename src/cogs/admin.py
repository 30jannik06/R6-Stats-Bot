import datetime

import discord
from discord import app_commands
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
    @app_commands.choices(platform=[
        app_commands.Choice(name="❌ WICHTIG", value="❌ WICHTIG"),
        app_commands.Choice(name="🚨 DRINGEND", value="🚨 DRINGEND"),
        app_commands.Choice(name="🔍 IN ÜBERPRÜFUNG", value="🔍 IN ÜBERPRÜFUNG"),
        app_commands.Choice(name="🛠️ TECHNISCHE HILFE", value="🛠️ TECHNISCHE HILFE"),
        app_commands.Choice(name="🚧 IN ARBEIT", value="🚧 IN ARBEIT")
    ])
    async def stats(self, interaction: discord.Interaction, player_name: str, platform: str):
        stats = await get_player_stats(player_name, platform="uplay")
        #PLATFORM_URL_NAMES = {"uplay": "OSBOR_PC_LNCH_A", "psn": "OSBOR_PS4_LNCH_A", "xbl": "OSBOR_XBOXONE_LNCH_A", "xplay": "OSBOR_XPLAY_LNCH_A"}
        #print(stats)
        
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
        
        SEASON_NAMES = {
            3: "Black Ice",
            4: "Dust Line",
            5: "Skull Rain",
            6: "Red Crow",
            7: "Velvet Shell",
            8: "Health",
            9: "Blood Orchid",
            10: "White Noise",
            11: "Chimera",
            12: "Para Bellum",
            13: "Grim Sky",
            14: "Wind Bastion",
            15: "Burnt Horizon",
            16: "Phantom Sight",
            17: "Ember Rise",
            18: "Shifting Tides",
            19: "Void Edge",
            20: "Steel Wave",
            21: "Shadow Legacy",
            22: "Neon Dawn",
            23: "Crimson Heist",
            24: "North Star",
            25: "Crystal Guard",
            26: "High Calibre",
            27: "Demon Veil",
            28: "Vector Glare",
            29: "Brutal Swarm",
            30: "Solar Raid",
            31: "Commanding Force",
            32: "Dread Factor",
            33: "Heavy Mettle",
            34: "Operation Deadly Omen",
            35: "Operation Twin Shells",
            36: "Operation Collision Point"
        }

        seasonName = SEASON_NAMES.get(stats.ranked_profile.season_id, "Unknown Season")
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
        
    @discord.app_commands.command(name="rank", description="Get actual Rank from User")
    async def rank(self, interaction: discord.Interaction, player_name: str):
        stats = await get_player_stats(player_name)
        
        name: str = stats.name
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
        
        rankEmbed: discord.Embed = discord.Embed(description=f'Player information: **{name}**')
        rankEmbed.set_author(icon_url=stats.profile_pic_url, name=f'{name}')
        rankEmbed.add_field(name="Season Rank:", value=nowRank)
        rankEmbed.set_thumbnail(url=rankImg)
        
        await interaction.response.send_message(embed=rankEmbed)
    
async def setup(client):
    await client.add_cog(Admin(client))
    command(f'🛠️ Loaded Admin Slash Commands')

#TODO:[WIP] /stats <Spielername> – Zeigt die allgemeinen Statistiken eines Spielers.
#TODO:[WIP] /rank <Spielername> – Gibt den aktuellen Rang des Spielers aus.
#TODO:[NOSTARTED] /loadout <Spielername> – Zeigt die bevorzugte Ausrüstung eines Spielers.
#TODO:[NOSTARTED] /operator <Spielername> – Zeigt die meistgespielten Operatoren.
#TODO:[NOSTARTED] /matchhistory <Spielername> – Zeigt die letzten Matches des Spielers.
#TODO:[NOSTARTED] /leaderboard – Gibt eine Rangliste der besten Spieler aus.
#TODO:[NOSTARTED] /mmr <Spielername> – Zeigt das Matchmaking-Rating eines Spielers.
#TODO:[NOSTARTED] /seasonstats <Spielername> – Zeigt die aktuellen Season-Statistiken.
#TODO:[NOSTARTED] /kd <Spielername> – Gibt das K/D-Verhältnis aus.