# ╔══════════════════════════════════════════════════════════════════╗
# ║                                                                  ║
# ║                         CREATOR TAG                              ║
# ║                                                                  ║
# ║   Author:        30jannik06                                      ║
# ║   Date:          14.02.2025                                      ║
# ║   File:          check_permission_utils.py                       ║
# ║                                                                  ║
# ║   GitHub:        https://github.com/30jannik06                   ║
# ║   Discord:       https://discordapp.com/users/268084996235853824 ║
# ║                                                                  ║
# ╚══════════════════════════════════════════════════════════════════╝

import discord

async def check_permission(interaction: discord.Interaction, permission: str, error_message: str):
    
    '''
    Überprüft, ob der Benutzer eine bestimmte Berechtigung hat.
    
    :param interaction: Die Discord-Interaction
    :param permission: Die zu prüfende Berechtigung
    :param error_message: nachricht, die gesendet wird, wenn der benutzer keine Berechtigung hat
    :return: True, wenn die berechtigung vorhanden ist, sonst False
    '''
    
    if not getattr(interaction.user.guild_permissions, permission, False):
        await interaction.response.send_message(error_message, ephemeral=True)
        return False
    return True


'''
Code beispiel:
has_permission = await check_permission(interaction=interaction, permission="manage_channels", error_message="Du hast keine Berechtigung, um ein Ticket zu schließen.")
if not has_permission:
    return
'''