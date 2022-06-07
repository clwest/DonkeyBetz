from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

discord_token = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix='!')


@bot.command()
async def coin(cxt):
    
    """
    cxt = content about how the command was executed
    !coin will call the coin data
    """
    
    await cxt.send(cxt.guild)
    await cxt.send(cxt.author)
    await cxt.send(cxt.message.id)


@bot.command()
async def info(cxt):
    
    """
    cxt = content about how the command was executed
    !coin will call the coin data
    """
    
    await cxt.send(cxt.guild)
    await cxt.send(cxt.author)
    await cxt.send(cxt.message.id)
    await cxt.send(cxt.message.content)

bot.run(discord_token)