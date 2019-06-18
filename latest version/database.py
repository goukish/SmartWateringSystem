import MySQLdb as db

conn = db.connect('localhost', 'datacontrol', '123', 'smart_watering')

with conn:
    
    cur = conn.cursor()
    cur.execute("INSERT INTO moist_log VALUES(CURDATE(), CURTIME(), 10.45, 55, FALSE)")
    cur.execute("INSERT INTO moist_log VALUES(CURDATE(), CURTIME(), 15.00, 55, FALSE)")
    
    
    