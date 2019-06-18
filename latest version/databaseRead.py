import MySQLdb as db

conn = db.connect('localhost', 'datacontrol', '123', 'smart_watering')

with conn:
    
    cur = conn.cursor()
    cur.execute("SELECT * FROM moist_log")
    
    print("\nDate\t\tTime\t\tValue\t\tThreshold\tPassed")
    print("===============================================================")
    
    for reading in cur.fetchall():
        print(str(reading[0]) + "\t" + str(reading[1]) + "\t" + str(reading[2]) + "\t\t" + str(reading[3]) + "\t\t" + str(reading[4]))