# Author: BinaryBills
# Creation Date: December 25, 2023
# Date Modified: March 17, 2023
# Purpose:

import re
import discord
from discord.ext import commands
from discord import app_commands
from discord import ui
from config import settings
from config import sqlServer
from config.sqlServer import department_exists, course_exists

# Blacklist of domain names
domain_blacklist = ['chegg.com', 'tiktok.com', 'coursehero.com', 'brainly.com', 'facebook.com', 'twitter.com', 'tumblr.com' 'instagram.com', 'reddit.com', 'pinterest.com', 'tinder.com', 'pornhub.com', 'xvideos.com', 'xnxx.com']

async def add_resource(course_id, resource_name, resource_link, uploader_id):
    
    # Check if the resource link already exists in the database
    query = "SELECT * FROM academic_resources WHERE resource_link = ?"
    cursor = settings.conn.cursor()
    cursor.execute(query, (resource_link,))
    result = cursor.fetchone()

    # If the resource link already exists, return False
    if result:
        return False

    # Otherwise, add the resource and return True
    try:
        query = """INSERT INTO academic_resources (course_id, resource_name, resource_link, uploader_id) VALUES (?, ?, ?, ?)"""
        cursor.execute(query, (course_id, resource_name, resource_link, uploader_id))
        settings.conn.commit()
        sqlServer.print_table_contents(settings.conn, "academic_resources")
        return True
    except Exception as e:
        print(f"Error adding resource: {e}")
        return False

class myModal(ui.Modal, title="Upload a Study Resource"):
    field1 = ui.TextInput(label="Enter the Course:", placeholder="CIS, IMSE, GEOL,...", style=discord.TextStyle.short)
    field2 = ui.TextInput(label="Enter the Course Number:", placeholder="150,200, 350...", style=discord.TextStyle.short)
    field3 = ui.TextInput(label="Enter the Topic:", placeholder="Recursion, Theory of forms, Tension force...", max_length=50, style=discord.TextStyle.short)
    field4 = ui.TextInput(label="Enter the link to the resource:", placeholder="https://www.youtube.com/watch?v=4agL-MQq05E", max_length=120, style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            course_code = self.field1.value
            course_number = self.field2.value
            resource_name = self.field3.value
            link = self.field4.value
            uploader_id = interaction.user.id
            
            #Check if the link is valid
            url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
            if not url_pattern.match(link):
                await interaction.response.send_message("Please enter a valid link.")
                return
            
            #Check if the link is from a blacklisted domain
            if any(bl_domain in link for bl_domain in domain_blacklist):
                await interaction.response.send_message("The provided link is from a blacklisted domain.")
                return

            if not await department_exists(settings.conn, course_code):
                await interaction.response.send_message(f"Invalid department: {course_code}")
            elif not await course_exists(settings.conn, course_code, course_number):
                await interaction.response.send_message(f"Invalid course number: {course_number}")
            else:
                query = """
                    SELECT courses.id
                    FROM courses
                    JOIN departments ON courses.department_id = departments.id
                    WHERE departments.department_code = ? AND courses.course_number = ?
                """
                cursor = settings.conn.cursor()
                cursor.execute(query, (course_code, course_number))
                course_id = cursor.fetchone()
                
                if course_id:
                    course_id = course_id[0]
                    added = await add_resource(course_id, resource_name, link, uploader_id)
                
                    if added:
                     await interaction.response.send_message(f"Resource '{resource_name}' added for {course_code} {course_number}: {resource_name}")
                    else:
                     await interaction.response.send_message(f"The resource link already exists in the database.")
                else:
                    await interaction.response.send_message(f"An error occurred while adding the resource")
        except Exception as e:
            print(f"Error in on_submit: {e}")
            await interaction.response.send_message("An error occurred while processing your request. Please try again later.")

class Add(commands.Cog):
    """
    A cog that defines the "add" command for the bot.
    """
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="add", description="Adds a study resource to the WolverineStudyBot database!")
    async def add(self, interaction: discord.Interaction):
        await interaction.response.send_modal(myModal())

async def setup(client):
    await client.add_cog(Add(client))
