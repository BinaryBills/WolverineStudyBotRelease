# Author: BinaryBills
# Creation Date: January 8, 2023
# Date Modified: March 17, 2023
# Purpose: This file is responsible for loading the bot's sensitive data,
# connecting to the targeted SQL server, and adding all the tables to
# the database needed for the bot to function.

import os
from config import sqlServer
from config import sqlTable
from dotenv import load_dotenv
from datetime import datetime
from pytz import timezone
import asyncio

############################################
#         Figuring out time                #
############################################
def getTime():
    tz = timezone('EST')
    return str(datetime.now(tz)) 

############################################
#        Loading secret data               #
############################################
"""Loads data from .env to get the discord bot API key and SQL server credentials"""
load_dotenv()
TOKEN = os.getenv("DISCORD_API_TOKEN")

DB_FILE = "discord_bot.db"

############################################
#      Connecting to server                #
############################################
"""Connects and creates database if it does not already exist"""
try:
    conn = sqlServer.connect_to_sqlite_db(DB_FILE)
    sqlServer.create_tables(conn)
except Exception as e:
    print(f"Error connecting to SQLite DB: {e}")
    exit()

############################################
#    Populating Course & Departments       #
############################################
"""Initializing Course & Department Table with numbers"""
department_list = ['CIS', 'ENGR', 'IMSE', 'GEOL']
try:
     sqlServer.initialize_departments(conn, department_list)
     sqlServer.initialize_courses(conn, department_list)
    
except Exception as e:
    print(f"Error initializing departments and courses: {e}")
    
    
# Print the contents of the tables
sqlServer.print_table_contents(conn, "departments")
sqlServer.print_table_contents(conn, "courses")
sqlServer.print_table_contents(conn, "academic_resources")
