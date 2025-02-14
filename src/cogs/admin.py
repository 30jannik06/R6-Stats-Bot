# ╔══════════════════════════════════════════════════════════════════╗
# ║                                                                  ║
# ║                         CREATOR TAG                              ║
# ║                                                                  ║
# ║   Author:        30jannik06                                      ║
# ║   Date:          14.02.2025                                      ║
# ║   File:          admin.py                                        ║
# ║                                                                  ║
# ║   GitHub:        https://github.com/30jannik06                   ║
# ║   Discord:       https://discordapp.com/users/268084996235853824 ║
# ║                                                                  ║
# ╚══════════════════════════════════════════════════════════════════╝

import discord
from discord.ext import commands

from colorama import Fore
from helper.logging_utils import *

from dotenv import load_dotenv

load_dotenv()

class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client

    # region Commands

    # region Ping-Command
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong!')
    # endregion


    # endregion
async def setup(client):
    await client.add_cog(Admin(client))
    command(f'🛠️ Loaded Admin Slash Commands')