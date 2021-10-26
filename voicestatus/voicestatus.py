#!/usr/bin/env python3
__author__ = 'Hedius'
__license__ = 'GPLv3'

import asyncio
import sys
import threading
import os
import logging

from argparse import ArgumentParser

from StatusBot.StatusBot import StatusBot
from WidgetAPI.WidgetAPI import app
from waitress import serve


def start_bot_thread(token, load_all_members):
    """
    Start the discord bot in a isolated thread.
    :param token: bot token
    :param load_all_members: load all members or just members in voice
        channels.
    """
    bot = StatusBot(load_all_members)
    loop = asyncio.get_event_loop()
    loop.create_task(bot.start(token))
    thread_bot = threading.Thread(target=loop.run_forever)
    thread_bot.start()
    return thread_bot


def read_config():
    args = ArgumentParser(
        description=('Simple flask/nextcord app for generating a discord'
                     ' widget.json with discord user_ids in the name.'
                     ' Useful for better tracking of members in channels.'
                     ' You can overwrite the variables with environment '
                     'variables: VOICESTATUS_TOKEN, _HOST, _PORT, _LOAD_ALL.')
    )
    args.add_argument('-t', '--token', dest='token', required=False,
                      default=None,
                      help='Discord Bot Token')
    args.add_argument('-b', '--host', dest='host', default='0.0.0.0',
                      help='Host to bind to. (Default 0.0.0.0)')
    args.add_argument('-p', '--port', dest='port', default=8080,
                      type=int, help='Port to bind to. (Default 8080)')

    args.add_argument('-a', '--load-all-members', dest='load_all',
                      help='Load all members or only members in voice '
                           'channels.',
                      action='store_true', default=False)

    args = args.parse_args()
    token = os.getenv('VOICESTATUS_TOKEN', args.token)
    if not token:
        print('DISCORD BOT TOKEN NOT GIVEN!', file=sys.stderr)
        sys.exit(1)
    host = os.getenv('VOICESTATUS_HOST', args.host)
    port = int(os.getenv('VOICESTATUS_PORT', args.port))
    load_all = bool(os.getenv('VOICESTATUS_LOAD_ALL', args.load_all))
    return token, host, port, load_all


def main():
    token, host, port, load_all = read_config()

    logging.getLogger('waitress').setLevel(logging.DEBUG)

    # Start the discord bot in a thread
    start_bot_thread(token, load_all)
    # we will not join the bot thread -> kill it if flask crashes

    # run flask in the main thread
    serve(app, host=host, port=port, ident='VoiceStatus')


if __name__ == '__main__':
    main()
