#!/usr/bin/env python3

""" ursla """

import logging
import os
from pathlib import Path

import requests
from dotenv import load_dotenv
from flask import Flask
from flask_restful import Api, Resource, reqparse

import accountManager
import audioManager

# setup
if os.getenv('BOTKEY') is None:
    load_dotenv(str(Path(__file__).resolve().parents[0]) + '/keys.env')

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('sourceName')
parser.add_argument('displayID')

logging.basicConfig(level=logging.INFO, format=('%(asctime)s %(levelname)s %(name)s | %(message)s'))
logger = logging.getLogger('bot')
logger.setLevel('DEBUG')

NOT_OKAY_MSG = 'NOT OKAY :('

def activeVoiceChannels(bot=None):
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

        
        activeVcsId = ''
        for vc in activeVcs:
            activeVcsId = activeVcsId + str(vc.id) + ','

        logger.debug(activeVcsId)

        return activeVcsId

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

class account(Resource):
    ''' returns a free account token and bot status '''

    def get(self):
        return accountManager.getAccount()


class alive(Resource):
    ''' returns okay '''

    def get(self):
        return 'OKAY'

api.add_resource(index, '/')
api.add_resource(vcs, '/vcs')
api.add_resource(alive, '/alive')
api.add_resource(account, '/account')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=True)
