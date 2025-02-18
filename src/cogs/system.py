import datetime

import discord
from discord import app_commands
from discord.ext import commands

from helper.logging_utils import *
from helper.stats_utils import get_player_stats_data

from dotenv import load_dotenv

load_dotenv()

class System(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong!')
    
    @discord.app_commands.command(name="stats", description="Remove User from Ticket")
    @app_commands.choices(platform=[
        app_commands.Choice(name="💻 PC", value="uplay"),
        app_commands.Choice(name="❌ XBOX", value="xbl"),
        app_commands.Choice(name="➕ psn", value="psn"),
        app_commands.Choice(name="🕳 XPLAY", value="xplay")
    ])
    async def stats(self, interaction: discord.Interaction, platform: str,  player_name: str):
        try:
            stats = await get_player_stats_data(player_name=player_name, platform=platform)
            if not stats:
                await interaction.response.send_message("Spieler nicht gefunden oder keine Daten verfügbar.\nBeachte, dass du die richtige Plattform auswählst und den Namen korrekt schreibst.", ephemeral=True)
                return
        except Exception as e:
            await interaction.response.send_message(f'Spieler nicht gefunden oder keine Daten verfügbar.\nBeachte, dass du die richtige Plattform auswählst und den Namen korrekt schreibst.', ephemeral=True)
            return
        
        statsEmbed: discord.Embed = discord.Embed(description=f'Player information: **{stats["name"]}**')
        statsEmbed.set_author(icon_url=f'{stats["profilePic"]}', name=f'{stats["name"]}')
        statsEmbed.set_thumbnail(url=stats["rankImg"])
        
        statsEmbed.add_field(name="General:", value=f'Level: **{stats["level"]}**\n{platform}')
        statsEmbed.add_field(name="RP:", value=f'**{stats["nowRP"]}**\nMax **{stats["maxRP"]}**')
        statsEmbed.add_field(name="Rank:", value=f'**{stats["nowRank"]}**\nMax **{stats["maxRank"]}**')
        statsEmbed.add_field(name="Seasonal KD:", value=f'**{stats["seasonalKd"]}**\nKills **{stats["rankedKills"]}**\nDeaths **{stats["rankedDeaths"]}**')
        statsEmbed.add_field(name="Seasonal WL:", value=f'**{stats["seasonalWl"]}%**\nWins **{stats["rankedWins"]}**\nLosses **{stats["rankedLosses"]}**')
        
        
        statsEmbed.set_footer(text=f'{stats["seasonName"]} • {stats["year"]}')
        statsEmbed.timestamp = datetime.datetime.now(datetime.timezone.utc)
                
        await interaction.response.send_message(embed=statsEmbed)
        
    @discord.app_commands.command(name="rank", description="Get actual Rank from User")
    @app_commands.choices(platform=[
        app_commands.Choice(name="uplay", value="uplay"),
        app_commands.Choice(name="xbl", value="xbl"),
        app_commands.Choice(name="psn", value="psn"),
    ])
    async def rank(self, interaction: discord.Interaction, platform: str,  player_name: str):
        try:
            stats = await get_player_stats_data(player_name=player_name, platform=platform)
            if not stats:
                await interaction.response.send_message("Spieler nicht gefunden oder keine Daten verfügbar.", ephemeral=True)
                return
        except Exception as e:
            await interaction.response.send_message(f'Ein Fehler ist aufgetreten. Bitte versuche es später erneut.')
            return
        
        rankEmbed: discord.Embed = discord.Embed(description=f'Player information: **{stats["name"]}**')
        rankEmbed.set_author(icon_url=f'{stats["profilePic"]}', name=f'{stats["name"]}')
        rankEmbed.add_field(name="Season Rank:", value=f'{stats["nowRank"]}')
        rankEmbed.set_thumbnail(url=f'{stats["rankImg"]}')
        
        await interaction.response.send_message(embed=rankEmbed)
    
async def setup(client):
    await client.add_cog(System(client))
    command(f'🛠️ Loaded System Slash Commands')