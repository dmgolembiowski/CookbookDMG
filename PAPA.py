"""
P.A.P.A. (Personal Assisting Peripheral Application)

Powered by Discord, Google, and Wikipedia
Special Thanks to NanoDano @DevDungeon.com
"""
import discord
from discord import Game
from discord.ext import commands
from discord.ext.commands import Bot
import logging
import asyncio
# import aiohttp
# import random
# import requests
# import httplib2
# from oauth2.client.contrib import gce
# from apiclient.discover import build

class VoiceEntry:
    def __init__ (self, message, player):
        self.requester = message.author
        self.channel = message.channelself.player = player
    def __str__(self):
        fmt = '*{0.title}* uploaded by {0.uploader} and requested by {1.display_name}'
        duration = self.player.duration
        if duration:
            fmt = fmt + '[length: {0[0]}m {0[1]}s]'.format(divmod(duration, 60))
        return fmt.format(self.player, self.requester)

class VoiceState:
    def __init__ (self, bot):
        self.current = None
        self.voice = None
        self.bot = bot
        self.play_next_song = asyncio.Event()
        self.skip_votes = set()
        self.audio_player = self.bot.loop.create_task(self.audio_player_task())
    def is_playing (self):
        if self.voice is None or self.current is None:
            return False
        player = self.current.player
        return not player.is_done()
    
    @property
    def player (self):
        return self.current.player

    def skip (self):
        self.skip_votes.clear()
        if self.is_playing():
            self.player.stop()
    def toggle_next (self):
        self.bot.loop.call_soon_threadsafe(self.play_next_song.set)
    async def audio_player_task(self):
        while True:
            self.play_next_song.clear()
            self.current = await self.songs.get()
            await self.bot.send_message(self.current.channel, 'Now playing: ' + str(self.current))
            self.current.player.start()
            await self.play_next_song.wait()

class Music:
# Voice-related commands. Works in multiple servers at once.
    def __init__ (self, bot):
        self.bot = bot
        self.voice_states = {}
    def get_voice_state (self, server):
        state = self.voice_status.get(server.id)
        if state is None:
            state = VoiceState(self.bot)
            self.voice_states[server.id] = state
        return state
    async def create_voice_client(self, channel):
        voice = await self.bot.join_voice_channel(channel)
        state = self.get_voice_state(channel.server)
        state.voice = voice
    def __unload(self):
        for state in self.voice_states.values():
            try:
                state.audio_player.cancel()
                if state.voice:
                    self.bot.loop.create_create_task(state.voice.disconnect())
            except:
                pass

@commands.command(pass_context = True, no_pm = True)
async def join (self, ctx, *, channel = discord.Channel):
    """joins a voice channel"""
    try:
        await self.create_voice_client(channel)
    except discord.ClientException:
        await self.bot.say('P.A.P.A. is already in another voice channel. How strange...')
    except discord.InvalidArgument:
        await self.bot.say('P.A.P.A. laughed at you. "I canny talk here!"')
    else:
        await self.bot.say('P.A.P.A can theoretically play audio in: '+ channel.name)

@commands.command(pass_context = True, no_pm = True)
async def summon (self, ctx):
    """Summons P.A.P.A. to join the voice channel."""
    summoned_channel = ctx.message.author.voice_channel 
    if summoned_channel is None:
        await self.bot.say('P.A.P.A. noticed David chasing after butterflies instead of joining the voice lobby. He sighed...')
        return False
    state = self.get_voice_state(ctx.message.server)
    if state.voice is None:
        state.voice = await self.bot.join_voice_channel(summoned_channel)
    else:
        await state.voice.move_to(summoned_channel)
    return True


# Write the logs to a file called discord.log.
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename = 'discord.log', encoding = 'utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s'))
logger.addHandler(handler)

# This might need to go near the beginning
TOKEN = "NDU1ODQ0OTkxNDIwMzM0MDgx.DhKicA.fDge8VKQNo_RoZ3s6CEldFu6b1Y"
BOT_PREFIX ="papa "
client = Bot(command_prefix = BOT_PREFIX)
bot = commands.Bot(command_prefix = BOT_PREFIX, description = 'P.A.P.A. on Discord')
"""bot.add_cog(Music(bot))"""
"""
# Google Stuff here
async def fetch(client):
    async with client.get('http://python.org') as repo:
        assert resp.status == 200
        return await resp.text()

async def main2(loop2):
    async with aiohttp.ClientSessionIO(loop=loop2) as client:
        html = await fetch(client)
        print(html)
        print(client)
 loop2 = asyncio.get_event_loop()
 loop2.run_until_complete(main2(loop2))
"""
# Maybe put this near the end...?
@asyncio.coroutine
def main_task():
    yield from client.login(TOKEN)
    # The next line is a coroutine function that creates a websocket connection and listens to messages from discord
    yield from client.connect()
    yield from bot.run(TOKEN)

@client.async_event
def on_ready():
    print('Wecome, ' + client.user.name + ' ' + client.user.id)
    print('______________________________________')
    print('P.A.P.A. is online and preparing services...')

loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(main_task())
except:
    # This next line might need to be changed with the 'heartbeat' functionality
    loop.run_until_complete(client.logout())
    # May be able to specify parameters that make client.logout() true, i.e. "forceShutdown == true" that normally has a default bool value of "false"
finally:
    loop.close
