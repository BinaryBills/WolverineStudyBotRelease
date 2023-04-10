#Author: BinaryBills
#Creation Date: January 8, 2022
#Date Modified: January 17, 2022
#Purpose: WolverineStudyBot is a Discord bot designed to help University of 
#Michigan student chatrooms by providing a simplistic moderation 
#system, facilitating a database that students can use to archive helpful 
#academic resources, and increasing student engagement. 
import os
import asyncio
import discord
from discord.ext import commands
from config import settings

#Assigns the bot's prefix for commands, permissions, and disables the default help command. 
client = commands.Bot(command_prefix = '!', intents=discord.Intents.all(), help_command = None)

async def load():
  """Loads the classes in the cog folder which encapsulates all the bot functionalities"""
  for filename in os.listdir('./cogs'):
     if filename.endswith('.py'):
         await client.load_extension(f'cogs.{filename[:-3]}')

async def main():
    """Calls the load function then launches the discord bot"""
    await load()
    await client.start(settings.TOKEN)

asyncio.run(main())