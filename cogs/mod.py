#Author: BinaryBills
#Creation Date: February 1, 2023
#Date Modified: February 11, 2023
#Purpose:
import discord
from discord.ext import commands
from discord import app_commands
from discord.app_commands import AppCommandError
import asyncio
import datetime

async def is_owner(interaction: discord.Interaction, member: discord.Member):
        if member.id == interaction.guild.owner_id:
            return True
        return False
    
class mod(commands.Cog):
    def __init__(self,client):
        self.client = client
        
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.bot_has_permissions(manage_messages = True)
    @app_commands.command(name = "clear", description = "Clears a specified amount of messages")
    async def clear(self, interaction: discord.Interaction, amount : int):
     await interaction.response.defer(ephemeral = True) 
     if amount < 1: 
        await interaction.followup.send(f"{interaction.user.mention}, you must specify a positive integer")
     elif amount > 100:
        await interaction.followup.send(f"{interaction.user.mention}, you cannot delete more than 100 messages at a time")
     else:
        messages = []
        async for message in interaction.channel.history(limit=amount):
            messages.append(message)
        if len(messages) == 0:
            await interaction.followup.send(f"{interaction.user.mention}, there are no messages to delete.")
            return
        deleted = 0
        for x in range(0, amount):
            if x >= len(messages):
                break
            try:
                await messages[x].delete()
                deleted += 1
                if (x % 13 == 0):  
                    await asyncio.sleep(2) 
            except discord.NotFound:
                continue
        await interaction.followup.send(f"{interaction.user.mention}, the previous **{deleted} messages** have been removed!")


    @app_commands.checks.has_permissions(kick_members=True)
    @app_commands.checks.bot_has_permissions(kick_members = True)
    @app_commands.command(name = "kick", description = "Kicks a user")
    async def kick(self, interaction: discord.Interaction, member:discord.Member, reason:str):
     temp = member
     if await is_owner(interaction, member) == False and (interaction.user.id != member.id) and (not member.guild_permissions.kick_members):
        await interaction.guild.kick(member)
        await interaction.response.send_message(f"{temp.mention} has been kicked! Reason: {reason}!")
     else:
        await interaction.response.send_message("User specified is a privileged user or has the kick members permission!")
         
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.checks.bot_has_permissions(ban_members = True)
    @app_commands.command(name = "ban", description = "Bans a user")
    async def ban(self, interaction: discord.Interaction, member:discord.Member, reason:str):
          temp = member
          if await is_owner(interaction, member) == False and (interaction.user.id != member.id) and (not member.guild_permissions.ban_members):
           await interaction.guild.ban(member)
           await interaction.response.send_message(f"{temp.mention} has been banned! Reason: {reason}!")
          else:
              await interaction.response.send_message("User specified is a privileged user or has the ban members permission!")
    
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.bot_has_permissions(manage_messages=True)
    @app_commands.checks.bot_has_permissions(moderate_members=True)
    @app_commands.command(name="mute", description="Mutes a user")
    async def mute(self, interaction: discord.Interaction, member: discord.Member, seconds: int = 0, minutes: int = 0, hours: int = 0, days: int = 0, reason: str = None):
      if await is_owner(interaction, member) == False and (interaction.user.id != member.id) and (not member.guild_permissions.manage_messages):
         duration_seconds = (days * 24 * 60 * 60) + (hours * 60 * 60) + (minutes * 60) + seconds
     
         if duration_seconds > 2419200:
          await interaction.response.send_message("The time you entered exceeds the maximum of 28 days!")
          return
   
         if duration_seconds < 0:
          await interaction.response.send_message("Please enter a positive integer!")
          return
          
         
         duration = datetime.timedelta(seconds=seconds, minutes=minutes, hours=hours, days=days)
         await member.timeout(duration, reason=reason)
         await interaction.response.send_message(f'{member.mention} was timeouted for {duration}', ephemeral=True)
        
      else:
        await interaction.response.send_message("User specified is a priviledged user!")
        
        
        return
    
    
        
    #all errors will be handled here 
    async def cog_app_command_error(self, interaction: discord.Interaction, error: AppCommandError):
        print("This error was handled!")
        await interaction.response.send_message(f"Sorry {interaction.user.mention}, but you or the bot lack the permissions to access this command! An error of another type could have also occurred!")
              
async def setup(client):
    await client.add_cog(mod(client))
