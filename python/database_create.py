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
    isAdmin INT(0) NOT NULL,
    allowedZones VARCHAR);""")
    
    cursor.execute("""CREATE TABLE nonDefaultDates (
    schedule_date DATE NOT NULL,
    schedule_label TEXT NOT NULL);""")

    cursor.execute("""CREATE TABLE schedules (
    schedule_label TEXT NOT NULL,
    schedule_entries TEXT NOT NULL);""") # Serialize ARRAYS to TEXT
    
    cursor.execute("""CREATE TABLE schedule_entries (
    schedule_label TEXT NOT NULL,
    schedule_time_to_ring TEXT NOT NULL,
    schedule_bellsound_filename TEXT NOT NULL);""") # Serialize ARRAYS to TEXT
    
    cursor.execute("""CREATE TABLE zones (
    zone_label TEXT NOT NULL,
    zone_bell_extension TEXT NOT NULL,
    zone_sip_remote_server TEXT NOT NULL,
    zone_sip_port TEXT NOT NULL,
    zone_sip_extension TEXT NOT NULL,
    zone_sip_password TEXT NOT NULL);""")

    # Insert the admin data into the table
    cursor.execute("""
    INSERT INTO userTable (username, password, isAdmin, allowedZones) 
    VALUES (?, ?, ?, ?);
    """, ('admin', 'password', True, '[]'))
    
    # Temp data
    cursor.execute("""
    INSERT INTO zones (zone_label, zone_bell_extension, zone_sip_remote_server, zone_sip_port, zone_sip_extension, zone_sip_password) 
    VALUES (?, ?, ?, ?, ?, ?);
    """, ('ExampleZone0', '6001', "10.10.10.10", "5060", "9100", "passwordsecretkey"))
     
     
    cursor.execute("""
    INSERT INTO zones (zone_label, zone_bell_extension, zone_sip_remote_server, zone_sip_port, zone_sip_extension, zone_sip_password) 
    VALUES (?, ?, ?, ?, ?, ?);
    """, ('ExampleZone1', '6001', "10.10.10.10", "5060", "9100", "passwordsecretkey"))
     
     
    cursor.execute("""
    INSERT INTO zones (zone_label, zone_bell_extension, zone_sip_remote_server, zone_sip_port, zone_sip_extension, zone_sip_password) 
    VALUES (?, ?, ?, ?, ?, ?);
    """, ('ExampleZone2', '6001', "10.10.10.10", "5060", "9100", "passwordsecretkey"))
     
     
    databaseConnection.commit()
    databaseConnection.close()

