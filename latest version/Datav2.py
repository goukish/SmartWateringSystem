import serial
import socket, sys, time
import MySQLdb as db

class DataController:
  
  def __init__(self):  
    self.moistThreshold = 0
    self.rainThreshold = 0
    self.MoistureLevelRaw = 0
    self.MoistureLevelPercent = 0
    self.RainLevelRaw = 0
    self.raining = 0

#sets Threshold if value is valid and assigns it
  def setMoistThreshold(self,i):
        if i <= 100:
          if i >= 0:
            moistThreshold = i
            #print('Threshold Test:')
            return True
             
        else: 
          return False
            

#sets Threshold if value is valid and assigns it
  def setRainThreshold(self,i):
        if (i <= 100 and i >=0):
            rainThreshold = i
            return True
        else: 
            return False
            
            
#  checks if moisture percent is valid and assigns it 
  def moistureinPercent(self,j):
        if j <=100:
          if j >=0:
            MoistureLevelPercent = j
            print('Moisture Level Test:')
            print('valid moistureLevel : ',MoistureLevelPercent)
           
        else:
          print('invalid moistureLevel', j)
          
  #checks if raining or not            
  def isRaining(self,i):
    if i <= 100:
      if i >= 25:
        Raining = i
        return True
         
    else: 
      return False  
    
    
  def isDry(self,i):
      if i <= 100:
        if i <= 20:
          Moisture = i
          return True
           
      else: 
        return False
    
    
    


# MAIN


d1 = DataController()
#d1.setMoistThreshold(25)
#d1.setRainThreshold(45)

#udp setup
host = "10.0.0.21"
textport = 2004
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = int(textport)
server_address = (host, port)

#arduino setup
ser = serial.Serial('/dev/ttyACM0', 9600)

#db setup
conn = db.connect('localhost', 'datacontrol', '123', 'smart_watering')


while 1:
    
    str = ser.readline()
    str = str.decode("utf-8")
    soil, rain = str.split(":")
    print(soil)
    print(rain)
    soil = float(soil)
    rain = float(rain)
    
    raining = d1.isRaining(rain)
    dry = d1.isDry(soil)
    
    if raining:
      #send udp message
      print("raining")
      data = "RainLimPassed"
      s.sendto(data.encode('utf-8'), server_address)
      
    elif (not raining) and (dry):
      #send opposite message
      print("not raining and not moist")
      data = "ManualOpen"
      s.sendto(data.encode('utf-8'), server_address)
#    if d1.isDry(soil):
 #     #send udp message
      #define isdry
  #    print("soil is dry af")
   #   data = "ManualOpen"
    #  s.sendto(data.encode('utf-8'), server_address)
    
    elif not dry:
      #send close message
      print("soil is moist")
      data = "MoistureLimPassed"
      s.sendto(data.encode('utf-8'), server_address)
      
    
    with conn:
    
        cur = conn.cursor()
        cur.execute("INSERT INTO rain_log VALUES(CURDATE(), CURTIME(), %d, %d, %r)" % (rain, 25, raining))
        cur.execute("INSERT INTO moist_log VALUES(CURDATE(), CURTIME(), %d, %d, %r)" % (soil, 20, not dry))
