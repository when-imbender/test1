#imports
import discord  #api
import keep_alive  #keeps our bot alive from the keep_alive.py file
import asyncio   #creating loop tasks etc 
import json  #to write db to a json file  #to check discord api for limits/bans
import random
import requests
from discord.ext import tasks, commands
from discord.utils import get


import websocket #pip install websocket-client

from pprint import pprint
import time
api_key = 'ad78b293189aaf1cde5352cc5cdec444'
channel_id = '631f7411d294a3934ede457e'

def on_error(ws, error):
    print(error)

def on_open(ws):
    # join the specified channel when the connection is established
    join_data = {
        'method': 'join',
        'params': {
            'channelId': channel_id
        },
        'id': 1
    }
    pprint('trying to join')
    ws.send(json.dumps(join_data))

    

def on_message(ws, message1):
    message_data = json.loads(message1)
    pprint(message_data)
    if message_data['method'] == 'keepAwake':
        print('keepalive')
        # respond to 'keepAwake' message with 'stayAwake' message
        stay_awake_data = {
            'jsonrpc': '2.0',
            'method': 'stayAwake',
            'params': {
                'date': str(int(time.time() * 1000))
            }
        }
        pprint(stay_awake_data)
        pprint(json.dumps(stay_awake_data))
        ws.send(json.dumps(stay_awake_data))
        #message_text = 'another keepalive received. fun.'
        #message_data = {
            #"jsonrpc": "2.0",
            #"method": "pushMessage",
            #"params": {
                #'payload': message_text
            #}
        #}
        #ws.send(json.dumps(message_data))
        update_user = {
            "jsonrpc": "2.0",
            "method": "editUser",
            "params": {
                "displayName": "GR Bot",
                "image": "https://app.rvrb.one/static/6307b6c6f07c2a50d46e6f8b_image.gif",
                "djImage": "https://app.rvrb.one/static/6307b6c6f07c2a50d46e6f8b_image.gif",
                "thumbsUpImage": "https://app.rvrb.one/static/6307b6c6f07c2a50d46e6f8b_image.gif",
                "thumbsDownImage": "https://app.rvrb.one/static/6307b6c6f07c2a50d46e6f8b_image.gif",
                "queueSettings": {
                    "newTracksToTop": False
                },
                "profileSettings": {},
                "theme": "dark",
                "bio": "where go die"
            },
            "id": 1
            }
        ws.send(json.dumps(update_user))
    elif message_data['method'] == 'pushChannelMessage':
        pprint(message_data)


websocket.enableTrace(True) 
ws = websocket.WebSocketApp(f'wss://app.rvrb.one/ws-bot?apiKey={api_key}',
                            on_error=on_error,
                            on_open=on_open,
                            on_message=on_message)

ws.run_forever(ping_interval=60)


r = requests.head(url="https://discord.com/api/v1")
try:
    print(
        f"You are being Rate Limited : {int(r.headers['Retry-After']) / 60} minutes left"
    )
except:
    print("No rate limit")

#-----------------------------------------
#declare client
intents = discord.Intents.all(
)  
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='&',  help_command=None)
#-----------------------------------------
@client.event
async def on_ready():
    print("\nGuerrilla Radio Bot Ready.\n")
    if not loop.is_running():
      loop.start()


keep_alive.keep_alive()
#-----------------------------------------
async def on_raw_reaction_add(payload):
    msg = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
    author = msg.author
    print(author.display_name)
#-----------------------------------------
@client.event
@commands.has_permissions(administrator=True)
#-----------------------------------------
#-----------------------------------------  	
async def on_message(message):
    #check for bots
    message.content = message.content.lower()
    if message.author.bot:
        return

	if message.content.startswith('!upvote'):
        await message.channel.send('sent')
        upvote = {'jsonrpc':'2.0','method':'vote','params':{'dope':True}}
        ws.send(json.dumps(upvote))
        rvrbmessage = {'jsonrpc':'2.0','method':'pushMessage','params':{'payload':f'Upvote from GR discord sent by: {message.author.display_name}','flair':None}}
        ws.send(json.dumps(rvrbmessage))
