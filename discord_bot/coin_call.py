from dotenv import load_dotenv
import vectorbt as vbt
import pandas as pd
import pandas_ta as ta
from datetime import datetime
import os
from alpaca_trade_api.rest import REST, TimeFrame
import discord

load_dotenv()

discord_token = os.getenv("DISCORD_TOKEN")

client = discord.Client()

@client.event

async def on_ready():
    print("bot is looking for data")
    


@client.event
async def on_message(message):
    
    if message.author == client.user:
        return
    
    if message.content.startswith("Hello"):
        await message.channel.send("Welcome to Donkey Betz")
        
        
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == "!coin":
        await message.channel.send("!coin will call the coin data")
        
@client.event
async def on_message(message):
    if message == client.user:
        return 
    if message.add_reaction("!coin is mooning"):
        await message.add_reaction("💰")
        
        
# @client.event
# async def on_reaction_add(reaction, user):
        
@client.event
async def on_message_edit(before, after):
    await before.channel.send(
        f"{before.author} edited a message. \n"
        f"Before: {before.content}\n"
        f"After: {after.content}")

client.run(discord_token)