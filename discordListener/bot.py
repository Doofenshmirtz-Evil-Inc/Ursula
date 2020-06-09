#!/usr/bin/env python3

""" ursla """

import logging
import os
import traceback
from pathlib import Path

import discord
from discord.ext import commands
from dotenv import load_dotenv

# setup
if os.getenv('BOTKEY') is None:
    load_dotenv(str(Path(__file__).resolve().parents[0]) + '/keys.env')

# Below cogs represents our folder our cogs are in. Following is the file name. So 'meme.py' in cogs, would be cogs.meme
# Think of it like a dot path import
initial_extensions = ['cogs.member', 'cogs.simple', 'cogs.call']

logging.basicConfig(level=logging.INFO, format=('%(asctime)s %(levelname)s %(name)s | %(message)s'))
logger = logging.getLogger('bot')
logger.setLevel('DEBUG')

description = '''ursla listens, ursla knows all'''
bot = commands.Bot(command_prefix='$', description=description)

# Here we load our extensions(cogs) listed above in [initial_extensions].
if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            logger.exception(f'Failed to load {extension}.')
            traceback.print_exc()

async def activeVoiceChannels(bot=bot):
    activeVCS = []
    for guild in bot.guilds:
        for vc in guild.voice_channels:
            if len(vc.members) > 1: # we dont want just one person sitting in silence
                # since theres people in the vc, check if theyre active
                logger.debug(f'voice channel {vc.name} in {vc.guild.name} has {len(vc.members)} users within, checking voice state')
                activeMembers = []
                for vcMember in vc.members:
                    if vcMember.voice.deaf == False and vcMember.voice.mute == False and vcMember.voice.self_mute == False and vcMember.voice.self_deaf == False:   
                        logger.debug(f'{vcMember.mention} is active')
                        activeMembers.append(vcMember)

                activeVCS.append(vc)
                
    logger.debug(f'found {len(activeVCS)} active voice channels')
    return activeVCS

# on start
@bot.event
async def on_ready():
    logger.info(f'Logged in as: {bot.user.name} - {bot.user.id}')
    logger.info(f'Version: {discord.__version__}')

    await activeVoiceChannels()

# login
bot.run(os.getenv('BOTKEY'))
