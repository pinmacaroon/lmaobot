import discord
import json
import requests
import os
from dotenv import load_dotenv
load_dotenv()

import utils
import commands
import economy

INTENTS = discord.Intents.default()

INTENTS.message_content = True
INTENTS.guild_messages = True
INTENTS.dm_messages = True
INTENTS.guild_reactions = True
INTENTS.guilds = True
INTENTS.dm_reactions = True
INTENTS.members = True
INTENTS.webhooks = True

CLIENT = discord.Client(intents=INTENTS)

@CLIENT.event
async def on_ready():
    print(f'logged in as {CLIENT.user}')
    for i in list(CLIENT.guilds):
        economy.initialize_economy_for_server(i)

@CLIENT.event
async def on_message(message: discord.Message):
    if message.author == CLIENT.user: return
    if not message.content.strip().startswith("l!"): return
    
    args: list = utils.parse_command(message.content.strip())
    command: str = args[0].lower()

    try:
        await commands.COMMANDS[command](message, args)
    except KeyError:
        await message.reply(
            f'the command `{command}` was not found! see `l!help`!'
        )

CLIENT.run(os.environ["TOKEN"])