import os
import time
import datetime
import glob
import MySQLdb
from time import strftime

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
moist_sensor = ' '

# Variables for MySQL
db = MySQLdb.connect(host="localhost", user="root",passwd="123", db="moist_database")
cur = db.cursor()

def moistRead():
    t = open(moist_database, 'r')
    lines = t.readlines()
    t.close()

    moist_output = lines[1].find('t=')
    if moist_output != -1:
        moist_string = lines[1].strip()[temp_output+2:]
        moist_c = float(temp_string)/1000.0
    return round(temp_c,1)

while True:
    moist = moistRead()
    print (moist)
    datetimeWrite = (time.strftime("%Y-%m-%d ") + time.strftime("%H:%M:%S"))
    print (datetimeWrite)
    sql = ("""INSERT INTO moist_Log (datetime,moisture) VALUES (%s,%s)""",(datetimeWrite,moist))
    try:
        print ("Writing to database...")
        # Execute the SQL command
        cur.execute(*sql)
        # Commit your changes in the database
        db.commit()
        print ("Write Complete")

    except:
        # Rollback in case there is any error
        db.rollback()
        print ("Failed writing to database")

    cur.close()
    db.close()
    break