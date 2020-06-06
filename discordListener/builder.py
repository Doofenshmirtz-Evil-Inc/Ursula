''' the ursula discord bot build manager. used to build and run dockerized ursla bots '''

# TODO: THIS IS NOT WORKING FIX THIS LATER
import argparse
import os
from pathlib import Path
import subprocess
import sys

DISCORD_LISTENER_PATH = str(Path(__file__).resolve().parents[0])

# setup argparser
parser = argparse.ArgumentParser(description='the ursula discord bot build manager. used to build and run dockerized ursla bots')
parser.add_argument('-b', '--build', help='build dockerized ursla bot', action='store_true')
parser.add_argument('-r', '--run', help='run latest dockerized ursla bot', action='store_true')

def build():
    # os.system(f'docker build -t ursulaListener {DISCORD_LISTENER_PATH}')
    # subprocess.call(['docker', 'build', '-t', 'ursulalistener', DISCORD_LISTENER_PATH])
    process = subprocess.Popen(f'docker build -t ursulalistener {DISCORD_LISTENER_PATH}', stdout=subprocess.PIPE)
    for c in iter(lambda: process.stdout.read(1), b''):
        sys.stdout.write(c)

def run():
    os.system('docker run --env-file keys.env ursulalistener')

if __name__ == "__main__":
    args = parser.parse_args()

    if args.build:
        build()
    elif args.run:
        run()
    else:
        print('the ursula discord bot build manager. used to build and run dockerized ursla bots. enter builder.py -h for help')
