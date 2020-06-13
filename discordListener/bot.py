#!/usr/bin/env python3

""" ursla """

import logging
import os
import threading
from pathlib import Path

import discord
import requests
from discord.ext import commands
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse

# setup
if os.getenv('BOTKEY') is None:
    load_dotenv(str(Path(__file__).resolve().parents[0]) + '/keys.env')

app = Flask(__name__)
api = Api(app, prefix="/api/v1")
parser = reqparse.RequestParser()
parser.add_argument('sourceName')
parser.add_argument('displayID')

logging.basicConfig(level=logging.INFO, format=('%(asctime)s %(levelname)s %(name)s | %(message)s'))
logger = logging.getLogger('bot')
logger.setLevel('DEBUG')

NOT_OKAY_MSG = 'NOT OKAY :('
DESCRIPTION = '''ursula listens, ursula knows all'''
bot = commands.Bot(command_prefix='$', description=DESCRIPTION)

def activeVoiceChannels(bot=bot):
    activeVCS = []
    for guild in bot.guilds:
        for vc in guild.voice_channels:
            if len(vc.members) > 0: # we dont want just one person sitting in silence (0 is normally 1)
                # since theres people in the vc, check if theyre active
                logger.debug(f'voice channel {vc.name} in {vc.guild.name} has {len(vc.members)} users within, checking voice state')
                activeMembers = []
                for vcMember in vc.members:
                    if vcMember.voice.deaf == False and vcMember.voice.mute == False and vcMember.voice.self_mute == False and vcMember.voice.self_deaf == False:   
                        logger.debug(f'{vcMember.name} is active')
                        activeMembers.append(vcMember)

                activeVCS.append(vc)
                
    logger.debug(f'found {len(activeVCS)} active voice channels')
    return activeVCS

async def disconnectAll():
    vcs = bot.voice_clients
    for vc in vcs:
        await vc.disconnect()

# api

class index(Resource):
    """ oh, what fun an index is """

    def get(self):
        return 'Hello there. Ya shouldn\'t be here'

class vcs(Resource):
    """ return a list of active voice channel id's to the listener """

    def get(self):
        """ return a list of active voice channel id's to the listener """

        try:
            activeVcs = activeVoiceChannels()
        except:
            return NOT_OKAY_MSG

        logger.debug(activeVcs)
        
        activeVcsId = []
        for vc in activeVcs:
            activeVcsId.append(vc.id)
            logger.debug(vc.id)

        return jsonify(activeVcsId)

    def post(self):
        """ this is stuff i grabbed from my alexascreencontrol repo, ill change it later """

        args = parser.parse_args()
        logger.debug(args)

        try:
            if args['displayID'] == '1':
                url = 'f'
                data = {'destinationSourceName': args['sourceName']}
                r = requests.put(url, json=data, params=data)
            else:
              # http://dev.userful.com/rest/#displays__displayid__switch_put
                url = 'f'
                data = {'sourceName': args['sourceName']}
                r = requests.put(url, json=data)

        except requests.exceptions.RequestException as e:
            logger.error(e)
            return NOT_OKAY_MSG

        return 'OKAY'

api.add_resource(index, '/')
api.add_resource(vcs, '/vcs')

def runApp():
    app.run(host='0.0.0.0', port=5000, threaded=True)

# on start
@bot.event
async def on_ready():
    logger.info(f'Logged in as: {bot.user.name} - {bot.user.id}')
    logger.info(f'Version: {discord.__version__}')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('TOM FONGUS\'s CRAaaaZY Racoon (2002)'))

    # cleanup if it crashed or something earlier
    await disconnectAll()
    vcs = activeVoiceChannels()
    appThread = threading.Thread(target=runApp)
    appThread.start()

# login
def runBot():
    bot.run(os.getenv('BOTKEY'), bot=True)

if __name__ == "__main__":
    runBot()
