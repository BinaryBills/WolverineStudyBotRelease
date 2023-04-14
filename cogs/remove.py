#Author: BinaryBills
#Creation Date: April 9, 2023
#Date Modified: April 9, 2023
#Purpose: This file allow users to manage and remove their own academic resources from the database. 

import discord
from discord.ext import commands
from discord import app_commands
from discord import ui
from config import settings
from config import sqlServer
import asyncio

class Remove(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="remove", description="Remove a study resource that you added.")
    async def remove(self, interaction: discord.Interaction, resource_link: str):
        try:
            cursor = settings.conn.cursor()
            
            # Fetch the uploader ID from the database
            query = """SELECT uploader_id FROM academic_resources WHERE resource_link = ?"""
            cursor.execute(query, (resource_link,))
            result = cursor.fetchone()
            cursor.close()

            # If there's no such link in the database
            if not result:
                await interaction.response.send_message("No such resource link found.", ephemeral=True)
                return

            uploader_id = result[0]

            # Get the bot owner ID
            app_info = await self.client.application_info()
            owner_id = app_info.owner.id

            # Check if the user is the original uploader or the bot owner
            if str(interaction.user.id) == str(uploader_id) or interaction.user.id == owner_id:
                # Remove the resource link
                query = """DELETE FROM academic_resources WHERE resource_link = ?"""
                cursor = settings.conn.cursor()
                cursor.execute(query, (resource_link,))
                settings.conn.commit()
                cursor.close()

                await interaction.response.send_message(f"Successfully removed resource link: {resource_link}", ephemeral=True)
            else:
                await interaction.response.send_message("You do not have permission to remove this resource link.", ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message("Error: Unable to remove the resource link from the database.", ephemeral=True)

async def setup(client):
    await client.add_cog(Remove(client))
