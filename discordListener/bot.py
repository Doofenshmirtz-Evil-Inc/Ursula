#!/usr/bin/env python3

""" stock bot """

import asyncio
import logging
import os
import sched
import time
import traceback
import threading

import discord
from discord.ext import commands
from dotenv import load_dotenv

# setup
s = sched.scheduler(time.time, time.sleep)
if os.getenv('BOTKEY') is None:
    load_dotenv('keys.env')

# Below cogs represents our folder our cogs are in. Following is the file name. So 'meme.py' in cogs, would be cogs.meme
# Think of it like a dot path import
initial_extensions = ['cogs.member', 'cogs.simple']

logging.basicConfig(level=logging.INFO, format=(
    '%(asctime)s %(levelname)s %(name)s | %(message)s'))

logger = logging.getLogger('bot')
logger.setLevel(logging.DEBUG)

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

# on start
@bot.event
async def on_ready():
    logger.info(f'Logged in as: {bot.user.name} - {bot.user.id}')
    logger.info(f'Version: {discord.__version__}')

# login
bot.run(os.getenv('BOTKEY'))
