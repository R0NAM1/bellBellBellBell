import os, pathlib, sys, sqlite3
## Check if bellBellBellBell.db exists and if not, create!

databasePath = pathlib.Path("bellBellBellBell.db")
if databasePath.is_file():
    print("Database already exists locally, nothing to do!")
    sys.exit()
else:
    print("bellBellBellBell.db not found, creating database and filling in template!")

    databaseConnection = sqlite3.connect("bellBellBellBell.db")
    cursor = databaseConnection.cursor()
    
    # Create User Table
    cursor.execute("""CREATE TABLE IF NOT EXISTS userTable (
    username VARCHAR(50) NOT NULL,
    password VARCHAR(5000) NOT NULL,
    isAdmin INT(0) NOT NULL);""")
    
    cursor.execute("""CREATE TABLE nonDefaultDates (
    schedule_date DATE NOT NULL,
    schedule_label TEXT NOT NULL);""")

    cursor.execute("""CREATE TABLE schedules (
    schedule_label TEXT NOT NULL,
    schedule_entries TEXT NOT NULL);""") # Serialize ARRAYS to TEXT 

    # Insert the admin data into the table
    cursor.execute("""
    INSERT INTO userTable (username, password, isAdmin) 
    VALUES (?, ?, ?);
    """, ('admin', 'password', 1))
 
    databaseConnection.commit()
    databaseConnection.close()

