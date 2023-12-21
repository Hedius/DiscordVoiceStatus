#!/usr/bin/env python3
__author__ = 'Hedius'
__license__ = 'GPLv3'

import asyncio
import logging
import os
import sys
import threading
from argparse import ArgumentParser

from waitress import serve

from StatusBot.StatusBot import StatusBot
from WidgetAPI.WidgetAPI import app


def start_flask_app(host, port) -> threading.Thread:
    """
    Launch the flask app for serving the shared storage data
    in a thread.
    :return: thread
    """

    def server_flask():
        """
        Start the flask app. / Main logic of the thread.
        """
        logging.info('Serving flask app at '
                     f'{host}:{port}')
        serve(app, host=host, port=port, ident='VoiceStatus')

    flask_thread = threading.Thread(target=server_flask)
    flask_thread.start()
    return flask_thread


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
    load_all = os.getenv(
        'VOICESTATUS_LOAD_ALL',
        str(args.load_all)
    ).lower() in ('true', '1', 't')
    return token, host, port, load_all


def main():
    token, host, port, load_all = read_config()

    logging.getLogger('waitress').setLevel(logging.DEBUG)

    # run flask in a thread
    flask_thread = start_flask_app(host, port)

    bot = StatusBot(load_all, flask_thread)
    bot.run(token)


if __name__ == '__main__':
    main()
