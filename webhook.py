import sqlite3
import os
import urllib
from bs4 import BeautifulSoup
import urllib.request
from urllib.request import Request, urlopen, urlcleanup
from urllib.error import URLError
import json
from  builtins import any as b_any
from discord import Webhook, AsyncWebhookAdapter
import aiohttp
from datetime import datetime
import asyncio
import re
from botkey import Key
from recruitDb import DbApi

db = DbApi()
terms = db.listTerms() 

def fetch():
    url = 'https://us.battle.net/forums/en/wow/1011639/'
    
    results = []

    req = Request(url)
    try:
        urlcleanup() 
        response = urlopen(req)
    except URLError as e:
        if hasattr(e, 'reason'):
            print('   We failed to reach a server.')
            print('   Reason: ', e.reason)
        elif hasattr(e, 'code'):
            print('    The server couldn\'t fulfill the request.')
            print('    Error code: ', e.code)
        return None, None
    else:
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')

        # get text
        text = soup.findAll('a', attrs={'class':'ForumTopic'}) 

        for topic in text:
            title = topic.find('span', attrs={'class':'ForumTopic-title'})
            title = re.sub(r'[^\x00-\x7F]+',' ', title.text.strip())
            if re.search(r'^[^<>]+$', title) :
                results.append((topic['href'][21:], title))

        #print(results)
        #print(text)) #(["a"])

#       with open('webtest.txt', 'w') as f:
#           for tag in text:
#               for stuff in tag.contents:
#                   print(stuff)
#                   wqLines = list(filter(lambda x: 'ForumTopic' in x, stuff))
#                   for wqLine in wqLines:
#                       f.write(wqLine)

        return results

def process(data):

    loop =  asyncio.get_event_loop()  

    for topic in data:
        # If the topic wasn't sent yet
        if not db.checkTopic( topic[0] ):

            # Check if the topic has any term
            if matchTopic( terms, topic[1] ):

                # If wasn't sent, send Webhook             
                loop.run_until_complete( sendWebhook( topic[0] ) )  
        
                # Register the topic so it isn't sent again
                db.registerTopic( topic[0] )

def matchTopic(terms, title):
    title = title.lower()
    for term in terms:
        contains = True

        for word in term[1].split(' '):
            print('{0} in {1}'.format(word, title))            
            contains &= (word in title)
        if contains:
            return True
    return False

async def sendWebhook(topicId):
    print('New topic found ({0}), sending Webhook'.format(topicId))

    # Fetch Webhook URL
    webhookurl = Key().webhook() 

    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url('{0}'.format(webhookurl), adapter=AsyncWebhookAdapter(session))
        await webhook.send('https://us.battle.net/forums/en/wow/topic/{0}'.format(topicId), username='Perfect Raider Finder', avatar_url='https://i.imgur.com/x3pJPUD.png')

loop =  asyncio.get_event_loop()  

# Fetch and Process Topics if there are filter terms
if len(terms) > 0 :
    process(fetch())



loop.close()  