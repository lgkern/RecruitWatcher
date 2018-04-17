# -*- coding: utf-8 -*-

import discord
from discord import Forbidden
#from discord.ext import commands
import random
from botkey import Key
import sys
import logging
import time
from discord import HTTPException
from discord import utils
from discord import DMChannel
from recruitDb import DbApi

logging.basicConfig(level=logging.INFO)

client = discord.Client()

prefix = Key().prefix()

db = DbApi()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    
    # we do not want the bot to reply to itself
    if message.author == client.user or 'recruitment' not in message.channel.name:
        return
    
    if message.content.startswith(prefix+'add'):
        await addTerm(message)
        
    if message.content.startswith(prefix+'remove'):
        await removeTerm(message)

    if message.content.startswith(prefix+'list'):
        await list(message)

async def addTerm(message):
    db.addTerm(message.content[4+len(prefix):])

async def removeTerm(message):
    db.removeTerm(message.content[7+len(prefix):])
        
async def list(message):
    msg = db.listTermsString()
    await message.channel.send('```List of terms currently being searched for:\n{0}```'.format(msg))

client.run(Key().value())
