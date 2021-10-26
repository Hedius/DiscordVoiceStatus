__author__ = 'Hedius'
__license__ = 'GPLv3'

from nextcord.ext import commands, tasks

from ..SharedStorage import SharedStorage
from ..StatusBot import StatusBot


def setup(bot):
    bot.add_cog(FetchData(bot))


class FetchData(commands.Cog, name='User Linker'):
    def __init__(self, bot: StatusBot):
        self._bot = bot
        self._storage = SharedStorage()

        self.sync.start()

    @tasks.loop(seconds=30.0)
    async def sync(self):
        """
        Check all members regularly. Set inactive member to inactive.
        Sync tag etc.
        :return:
        """
        new_data = {}
        await self._bot.wait_until_ready()
        for guild in self._bot.guilds:
            guild_data = {
                'id': str(guild.id),
                'name': guild.name,
                'instant_invite': 'https://discord.e4gl.com',
                'channels': [],
                'members': [],
            }
            for channel in guild.voice_channels:
                channel_data = {
                    'id': str(channel.id),
                    'name': channel.name,
                    'position': channel.position
                }
                guild_data['channels'].append(channel_data)

            for member in guild.members:
                member_data = {
                    'id': str(member.id),
                    'username': member.name,
                    'discriminator': member.discriminator,
                    'avatar': None,
                    'avatar_url': member.avatar.url if member.avatar else None,
                    'status': str(member.status),
                }
                if member.nick:
                    member_data['nick'] = member.nick
                if member.voice:
                    member_data['channel_id'] = member.voice.channel.id
                    member_data['deaf'] = member.voice.deaf
                    member_data['mute'] = member.voice.mute
                    member_data['self_deaf'] = member.voice.self_deaf
                    member_data['self_mute'] = member.voice.self_mute
                    member_data['suppress'] = member.voice.suppress
                if self._bot.load_all_members or member.voice:
                    guild_data['members'].append(member_data)
            new_data[guild.id] = guild_data

        with self._storage.lock:
            self._storage.data = new_data
