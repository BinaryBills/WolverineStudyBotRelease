#Author: BinaryBills
#Creation Date: January 17, 2023
#Date Modified: January 18, 2023
#Purpose: This file's responsibility is to add users to the database and measure their engagement in a server.

import discord
from discord import app_commands
from discord.ext import commands
import platform
from config import settings
from config import sqlServer
import sqlite3
import random
from easy_pil import *

# Function to create a user card containing user's level and experience points (XP)
async def userCard(row, author, guild):
         #Get level and XP from the database
         try:
          levelStats = list(row)
          level = int(levelStats[1])
          xp = int(levelStats[2])
         except TypeError:
             level = 0
             xp = 0
         
        #Create a dictionary containing user stats
         userCard = {
             "name": f"{author}",
             "xp" : xp,
             "level" : level,
             "next_level_xp": 100,
             "percentage": xp,
            }
             
         #Create a background and profile picture for the user card
         background = Editor(Canvas((900,300), color = "#00294e"))
         profile_picture = await load_image_async(str(author.avatar.url))
         profile = Editor(profile_picture).resize((150,150)).circle_image()
         poppins = Font.poppins(size=40)
         poppins_small = Font.poppins(size=30)
         
         #Draw user card elements on the background
         card_right_shape = [(600,0), (750,300), (900,300), (900,0)]
         background.polygon(card_right_shape, color="#f2c514")
         background.paste(profile, (30,30))
       
         
         #Draw XP bar
         background.rectangle( (30,220), width = 650, height = 40, color = "#FFFFFF" )
         print("does it ever reach here")
         background.bar( (30,220), max_width=650, height=40, percentage = userCard["percentage"], color = "#282828", radius=0)
         background.text( (200,40), userCard["name"], font=poppins, color = "#f2c514")
         
        
         #Draw level and XP information
         background.rectangle( (200,100), width = 350, height=2, fill = "#f2c514")
         background.text(
             (200,130), 
             f"Level - {userCard['level']} | XP - {userCard['xp']}/{userCard['next_level_xp']}",
             font = poppins_small,
             color = "#f2c514",
         )
        
         #Save user card as an image file
         file = discord.File(fp=background.image_bytes, filename = "levelcard.png")
         return file
    
#Class to handle user engagement in a server
class userSystem(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    #Listener for new messages
    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            
            #Ignore messages from bots
            if message.author.bot:
                return
            
            #Get user and guild information
            author = message.author
            guild = message.guild
            row = await sqlServer.getSpecificRow(settings.conn, "discord_ID", author.id, "levels")

             #If user is not in the database, add them
            if row is None:
                print("Inserting new user...")
                sqlServer.execute_query(settings.conn, f"INSERT OR IGNORE INTO levels (discord_ID, level, xp, guild, global_ban_status) VALUES ({author.id}, 0, 0, {guild.id}, 0)")
                settings.conn.commit()
            else:
                print("Updating user...")
                level, xp = row[1], row[2]
                
                #Increment XP based on user's current level
                if level < 5:
                    xp += random.randint(1, 3)
                    sqlServer.execute_query(settings.conn, f"UPDATE levels SET xp = {xp} WHERE discord_ID = {author.id} AND guild = {guild.id}")
                    settings.conn.commit()
                else:
                    rand = random.randint(1, (level // 4))
                    if rand == 1:
                        xp += random.randint(1, 3)
                        sqlServer.execute_query(settings.conn, f"UPDATE levels SET xp = {xp} WHERE discord_ID = {author.id} AND guild = {guild.id}") 
                        settings.conn.commit()
                        
                # Check if the user has reached a new level, update level and reset XP in the database
                if xp >= 100:
                    level += 1
                    sqlServer.execute_query(settings.conn, f"UPDATE levels SET level = {level} WHERE discord_ID = {author.id} AND guild = {guild.id}")
                    settings.conn.commit()
                    sqlServer.execute_query(settings.conn, f"UPDATE levels SET xp = 0 WHERE discord_ID = {author.id} AND guild = {guild.id}")
                    settings.conn.commit()
                    file = await userCard(row, author, guild)
                    await message.channel.send(f"{author.mention} has leveled up to level **{level}**!")
        except Exception as e:
            print(f"An error occurred: {e}")

    #Slash command to check user's level in the guild
    @app_commands.command(name = "lvl", description = "Check your level in the guild!")
    async def level(self,interaction: discord.Interaction):
        author = interaction.user
        guild = interaction.guild.id
        row = await sqlServer.getSpecificRow(settings.conn, "discord_ID", author.id, "levels")
        print(row)

        #If the user is not in the database, prompt them they must send at least one message first.
        if (row == None):
            await interaction.response.send_message("You must send at least one message before accessing this command!")
        else:
            #Send the user's level card
            file = await userCard(row, author, guild)
            await interaction.response.send_message(file=file)

async def setup(client):
    await client.add_cog(userSystem(client))
