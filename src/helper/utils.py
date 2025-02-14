# ╔══════════════════════════════════════════════════════════════════╗
# ║                                                                  ║
# ║                         CREATOR TAG                              ║
# ║                                                                  ║
# ║   Author:        30jannik06                                      ║
# ║   Date:          14.02.2025                                      ║
# ║   File:          utils.py                                        ║
# ║                                                                  ║
# ║   GitHub:        https://github.com/30jannik06                   ║
# ║   Discord:       https://discordapp.com/users/268084996235853824 ║
# ║                                                                  ║
# ╚══════════════════════════════════════════════════════════════════╝

import os

from helper.logging_utils import command


def ensure_dir_exists(path):
    '''Ensures that a directory exists; created it if not.'''
    if not os.path.exists(path):
        os.makedirs(path)
        
async def load_cogs(client, cogs):
    for cog in cogs:
            try:
                await client.load_extension(f'cogs.{cog}')
            except Exception as e:
                print(e)
                
async def sync_commands(client):
    try:
        synced = await client.tree.sync()
        command(f'🔄 Synced {len(synced)} command(s)')
    except Exception as e:
        print(e)