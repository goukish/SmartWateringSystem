import os
import time
import datetime
import glob
import MySQLdb
from time import strftime

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
rain_sensor = ' '

# Variables for MySQL
db = MySQLdb.connect(host="localhost", user="root",passwd="123", db="rain_database")
cur = db.cursor()

def moistRead():
    t = open(rain_database, 'r')
    lines = t.readlines()
    t.close()

    rain_output = lines[1].find('t=')
    if rain_output != -1:
        rain_string = lines[1].strip()[temp_output+2:]
        rain_c = float(temp_string)/1000.0
    return round(temp_c,1)

while True:
    rain = rainRead()
    print (rain)
    datetimeWrite = (time.strftime("%Y-%m-%d ") + time.strftime("%H:%M:%S"))
    print (datetimeWrite)
    sql = ("""INSERT INTO moist_Log (datetime,rain) VALUES (%s,%s)""",(datetimeWrite,rain))
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