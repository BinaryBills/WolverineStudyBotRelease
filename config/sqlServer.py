# Author: BinaryBills
# Creation Date: January 8, 2023
# Date Modified: January 17, 2023
# Purpose: Functions used to open an active connection and send data to the SQLite server.

import sqlite3
from sqlite3 import Error
from config import settings
from config import courseNumbers
from config import sqlTable

def create_tables(connection):
    table_creation_commands = [
        sqlTable.departmentsTable,
        sqlTable.coursesTable,
        sqlTable.academicResTable,
        sqlTable.levels
    ]
    for command in table_creation_commands:
        execute_query(connection, command)
        
def is_table_empty(connection, table_name):
    cursor = connection.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]
    cursor.close()
    print(count)
    return count == 0

def print_table_contents(connection, table_name):
    cursor = connection.cursor()
    try:
        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)
        rows = cursor.fetchall()
        print(f"Contents of the '{table_name}' table:")
        for row in rows:
            print(row)
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        cursor.close()

async def department_exists(connection, department_code):
    query = f"SELECT COUNT(*) FROM departments WHERE department_code = '{department_code}'"
    cursor = connection.cursor()
    cursor.execute(query)
    count = cursor.fetchone()[0]
    return count > 0

async def course_exists(connection, department_code, course_number):
    query = f"""
        SELECT COUNT(*)
        FROM courses
        JOIN departments ON courses.department_id = departments.id
        WHERE departments.department_code = '{department_code}' AND courses.course_number = '{course_number}'
    """
    cursor = connection.cursor()
    cursor.execute(query)
    count = cursor.fetchone()[0]
    return count > 0


def connect_to_sqlite_db(db_file):
    """
    Given an SQLite database file, it connects to it and accesses its information.
    """
    connection = None
    try:
        connection = sqlite3.connect(db_file)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
        exit()
    return connection


def execute_query(connection, query, params=None, cursor=None):
    """
    Given an SQLite server and an SQL command, it sends a query to the server.
    """
    if cursor is None:
        cursor = connection.cursor()

    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        print(f"Command '{query}' processed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

    return cursor


def initialize_departments(conn, default_departments):
    """Given a department code, it inserts it into the SQL department table. This allows the developer to dynamically add departments as needed."""
    try:
        for department in default_departments:
            execute_query(conn, f"INSERT OR IGNORE INTO departments (department_code) VALUES ('{department}');")
    except sqlite3.Error as error:
        print(f"Error: {error}")


def initialize_courses(connection, department_list):
    # Insert courses if they don't already exist
    cursor = connection.cursor()

    try:
        for department_code in department_list:
            # Get the department_id for the given department_code
            dept_id_query = f"SELECT id FROM departments WHERE department_code = '{department_code}'"
            cursor = execute_query(connection, dept_id_query, cursor=cursor)
            department_id = cursor.fetchone()[0]

            course_numbers = courseNumbers.getCourseNumberList(department_code)

            for course_number in course_numbers:
                insert_query = f"""
                    INSERT OR IGNORE INTO courses (department_id, course_number)
                    VALUES ({department_id}, '{course_number}')
                """
                try:
                    cursor = execute_query(connection, insert_query, cursor=cursor)
                    print(f"Inserting course {department_code} {course_number}")
                except sqlite3.Error as error:
                    print(f"Error inserting course {department_code} {course_number}: {error}")

        # Commit the changes
        connection.commit()
        print("Courses initialized successfully")

    except sqlite3.Error as error:
        print(f"Error initializing courses: {error}")



async def sqlite_user_query(connection, query):
    """
    Given an SQLite server and an SQL command, a user can send a query to the server.
    """
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print(f"Command '{query}' processed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

async def getSpecificRow(connection, column_name, value, table_name):
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {table_name} WHERE {column_name} = ?", (value,))
    row = cursor.fetchone()
    cursor.close()
    return row

async def get_specific_row(connection, primary_key, input_value, table):
    """
    Gets an entire specified row given necessary data.
    """
    cursor = connection.cursor()
    try:
        query = f"SELECT * FROM {table} WHERE {primary_key} = {input_value}"
        cursor.execute(query)
        print(f"Command '{query}' processed successfully")
        return cursor.fetchone()
    except Error as e:
        print(f"The error '{e}' occurred")
