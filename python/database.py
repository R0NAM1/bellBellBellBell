import sqlite3, pathlib, time, sys

passwordRandomKey = 'ChangeMeToo!'
databasePath = "bellBellBellBell.db";

def doDatabaseQuery(callToMake):
    # IF we have an error, ignore and try again
    while True:
        try:
            myDatabase = sqlite3.connect('bellBellBellBell.db') 
            myCursor = myDatabase.cursor()
            myCursor.execute(callToMake)
            return myCursor.fetchall()
        except Exception as e:
            print(e)
            pass
        time.sleep(1)
        
def doDatabaseCommit(callToMake):
    # IF we have an error, ignore and try again
    while True:
        try:
            myDatabase = sqlite3.connect('bellBellBellBell.db') 
            myCursor = myDatabase.cursor()
            myCursor.execute(callToMake)
            myDatabase.commit()
            return True
        except Exception as e:
            print(e)
            pass
        time.sleep(1)
        
    
def checkIfDatabaseExists():
    databasePath = pathlib.Path("bellBellBellBell.db")
    if not databasePath.is_file():
        print("bellBellBellBell.db not found, cannot start program!")
        sys.exit(0)
