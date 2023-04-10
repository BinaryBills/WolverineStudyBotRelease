#Author: BinaryBills
#Creation Date: January 8, 2023
#Date Modified: January 17, 2023
#Purpose:The functionalities present in this file are for 
#front-end testing and setting up the bot. 

import discord
from discord import app_commands
from discord.ext import commands
import platform
from config import settings


class __setup__(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        """Sends logs to the terminal and syncs the slash command tree"""
        synced = await self.client.tree.sync()
        print("=================================================")
        print("Starting Bot...")
        print("Bot Name: " + self.client.user.name)
        print("Discord Version: " + discord.__version__)
        print("Python Version: " + str(platform.python_version()))
        print("Slash Commands Synced:", str(len(synced)))
        print(f'Status: {self.client.user} is currently online!')
        print("Current Time: " + settings.getTime())
        print("=================================================")
             
    @app_commands.command(name = "ping", description = "Displays the bot's ping")
    async def ping(self, interaction: discord.Interaction):
        """Tests the latency of the bot"""
        await interaction.response.send_message(f"Pong! {round(self.client.latency * 1000)}ms")
        
  
async def setup(client):
    await client.add_cog(__setup__(client))
    
