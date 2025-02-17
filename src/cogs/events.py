import os

import discord
from discord.ext import commands

from helper.logging_utils import event, join, leave
from helper.embed_utils import create_embed

from dotenv import load_dotenv
load_dotenv()


class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        join(f'{member} has joined the server.')
    
    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        leave(f'{member} has left the server.')
    
    #@commands.Cog.listener()
    #async def on_message_edit(self, before, after):
    #    log_channel = discord.utils.get(before.guild.text_channels, name='log')
    #    print(log_channel)
    #    if log_channel:
    #        await log_channel.send(
    #            f'Nachricht von `{before.author.name}` bearbeitet:\n**Vorher:** `{before.content}`\n**Nachher:** `{after.content}`')


    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        log_channel = discord.utils.get(channel.guild.text_channels, name='log')
        if log_channel:
            # Überprüfen, ob es sich um einen Textkanal oder Sprachkanal handelt
            if isinstance(channel, discord.TextChannel):
                textChannelEmbed = create_embed(title="Text Channel Creation", description=f"Der Textkanal {channel.mention} wurde erstellt.")
                await log_channel.send(embed=textChannelEmbed)
            elif isinstance(channel, discord.VoiceChannel):
                voiceChannelEmbed = create_embed(title="Voice Channel Creation", description=f"Der Sprachkanal {channel.mention} wurde erstellt.")
                await log_channel.send(embed=voiceChannelEmbed)
            # Überprüfen, ob es sich um eine Kategorie handelt
            elif isinstance(channel, discord.CategoryChannel):
                categoryEmbed = create_embed(title="Category Creation", description=f"Die Kategorie `{channel.name}` wurde erstellt.")
                await log_channel.send(embed=categoryEmbed)                

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        log_channel = discord.utils.get(channel.guild.text_channels, name='log')
        if log_channel:
            # Überprüfen, ob es sich um einen Textkanal oder Sprachkanal handelt
            if isinstance(channel, discord.TextChannel):
                textChannelEmbed = create_embed(title="Text Channel  Delete", description=f"Der Textkanal `{channel.name}` wurde gelöscht.")
                await log_channel.send(embed=textChannelEmbed)                       
            elif isinstance(channel, discord.VoiceChannel):
                voiceChannelEmbed = create_embed(title="Voice Channel  Delete", description=f"Der Sprachkanal `{channel.name}` wurde gelöscht.")
                await log_channel.send(embed=voiceChannelEmbed)                  
            # Überprüfen, ob es sich um eine Kategorie handelt
            elif isinstance(channel, discord.CategoryChannel):
                categoryEmbed = create_embed(title="Category Delete", description=f"Die Kategorie `{channel.name}` wurde gelöscht.")
                await log_channel.send(embed=categoryEmbed)    

async def setup(client):
    await client.add_cog(Events(client))
    event(f'🎉 Loaded Events')
