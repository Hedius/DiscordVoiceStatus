__author__ = 'Hedius'
__license__ = 'GPLv3'

import logging

import nextcord
from nextcord.ext import commands


class StatusBot(commands.Bot):
    """Bot for gathering active voice members."""

    def __init__(self, load_all_members, flask_thread):
        """
        Init the bot
        """
        self.flask_thread = flask_thread
        intents = nextcord.Intents.all()
        self.load_all_members = load_all_members

        super().__init__(command_prefix='NOTHING!!!',
                         description='Data gatherer',
                         intents=intents)
        self.load_extension('StatusBot.cogs.fetch')
        logging.info('Discord BOT up and running.')
