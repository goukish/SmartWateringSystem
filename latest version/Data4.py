import serial
import socket, sys, time
import MySQLdb as db
import urllib2



class DataController:
  
    # Initializing the attributes
    def __init__(self):  
        self.MoistThreshold = 0.00
        self.RainThreshold = 0.00



    # sets the moisture limit threshold if the value is valid and assigns it to the attribute MoistThreshold
    def setMoistThreshold(self, value):
        value = float(value)
        if ((value >= 0) and (value <= 100)):
            self.MoistThreshold = value
            return True
        else: 
          return False
        
        
    # sets the rain limit threshold if the value is valid and assigns it to the attribute RainThreshold
    def setRainThreshold(self, value):
        value = float(value)
        if ((value >= 0) and (value <= 100)):
            self.RainThreshold = value
            return True
        else: 
          return False
          
          
    #checks if it is raining or not            
    def isRaining(self, rainValue):
        if ((rainValue >= self.RainThreshold) and (rainValue <= 100)):
            return True
        else: 
          return False
        
    
    #checks if it is raining or not            
    def isMoist(self, moistValue):
        if ((moistValue >= self.MoistThreshold) and (moistValue <= 100)):
            return True
        else: 
          return False      





# ================== MAIN ================== #
        
dc = DataController()
dc.setMoistThreshold(5.00)
dc.setRainThreshold(35.00)
      

# UDP setup
host = "10.0.0.21"
textport = 2004
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = int(textport)
server_address = (host, port)


# Arduino USB serial setup
ser = serial.Serial('/dev/ttyACM0', 9600)


# Database connection setup
conn = db.connect('localhost', 'datacontrol', '123', 'smart_watering')


# Main loop
while 1:
    
    # Read the data printed from the Arduino to the serial
    str = ser.readline().decode("utf-8")  # Receive the sensor values in the format "xx:yy", where xx is the soil value, yy is the rain
    soil, rain = str.split(":")    # Split the string into the 2 variabes at the ":"
    soil = float(soil)    # Cast as float for inserting into db
    rain = float(rain)
    print("\nSoil: %.2f" % soil)
    print("Rain: %.2f" % rain)
    
    

    # Send instruction to Server.py based on data  
    if (not dc.isRaining(rain)) and (not dc.isMoist(soil)):
        print("Not raining, Soil not moist")
        data = "ManualOpen"
        s.sendto(data.encode('utf-8'), server_address)
      
    elif (dc.isRaining(rain)) and (dc.isMoist(soil)):
        print("Raining, Soil is moist")
        data = "RainLimPassed"
        s.sendto(data.encode('utf-8'), server_address)      
      
    elif dc.isRaining(rain):
        print("Raining, Soil not moist")
        data = "RainLimPassed"
        s.sendto(data.encode('utf-8'), server_address)
      
    elif dc.isMoist(soil):
        print("Not raining, Soil is moist")
        data = "MoistureLimPassed"
        s.sendto(data.encode('utf-8'), server_address)
      
    else:
        print("Error")
    
    
    
    # Enter rain/moisture data into database
    with conn:
    
        cur = conn.cursor()
        cur.execute("INSERT INTO rain_log VALUES(CURDATE(), CURTIME(), %f, %f)" % (rain, dc.RainThreshold))    # insert rain data into rain_log
        cur.execute("INSERT INTO moist_log VALUES(CURDATE(), CURTIME(), %f, %f)" % (soil, dc.MoistThreshold))    # insert soil data into moist_log


    
      
      
    