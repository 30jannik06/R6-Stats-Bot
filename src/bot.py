# ╔══════════════════════════════════════════════════════════════════╗
# ║                                                                  ║
# ║                         CREATOR TAG                              ║
# ║                                                                  ║
# ║   Author:        30jannik06                                      ║
# ║   Date:          14.02.2025                                      ║
# ║   File:          main.py                                         ║
# ║                                                                  ║
# ║   GitHub:        https://github.com/30jannik06                   ║
# ║   Discord:       https://discordapp.com/users/268084996235853824 ║
# ║                                                                  ║
# ╚══════════════════════════════════════════════════════════════════╝

import os
import platform

import discord
from discord.ext import commands
from dotenv import load_dotenv

from colorama import Fore
from helper.logging_utils import *
from helper.utils import load_cogs, sync_commands

load_dotenv()

BOTTOKEN = os.getenv("TOKEN")

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

async def load_extension():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f'cogs.{filename[:-3]}')
            
async def main():
    async with client:
        await load_extension()
        
def clear_console():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")
        
@client.event
async def on_ready():
    cogList: list[str] = ['admin']

    clear_console()
    print('╔════════════════════════════════════════════════════════╗')
    print(Fore.BLUE + ""
                        f"{Fore.WHITE}║{Fore.YELLOW}██████╗  ██████╗ ████████╗\n"
                        f"{Fore.WHITE}║{Fore.YELLOW}██╔══██╗██╔═══██╗╚══██╔══╝\n"
                        f"{Fore.WHITE}║{Fore.YELLOW}██████╔╝██║   ██║   ██║   \n"
                        f"{Fore.WHITE}║{Fore.YELLOW}██╔══██╗██║   ██║   ██║   \n"
                        f"{Fore.WHITE}║{Fore.YELLOW}██████╔╝╚██████╔╝   ██║   \n"
                        f"{Fore.WHITE}║{Fore.YELLOW}╚═════╝  ╚═════╝    ╚═╝   \n"
                        f"{Fore.WHITE}║{Fore.YELLOW}" + Fore.RESET)
    info("🚀 Bot is ready!")
    info(f'🤖 Logged in as {client.user}')

    await load_cogs(client, cogList)
    await sync_commands(client)
        
    print('╚════════════════════════════════════════════════════════╝')
    

client.run(BOTTOKEN)