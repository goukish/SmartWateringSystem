import serial
import socket, sys, time

class DataController:
  
  def __init__(self):  
    self.Threshold = 0
    self.MoistureLevelRaw = 0
    self.MoistureLevelPercent = 0
    self.RainLevelRaw = 0
    self.raining = 0

#sets Threshold if value is valid and assigns it
  def setThreshold(self,i):
        if i <= 100:
          if i >= 0:
            Threshold = i
            #print('Threshold Test:')
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
      if i >= 50:
        Raining = i
        return True
         
    else: 
      return False  
    
  def isDry(self,i):
      if i <= 100:
        if i <= self.Threshold:
          Moisture = i
          return True
           
      else: 
        return False
        
d1 = DataController()
d1.setThreshold(15)

#udp setup
host = "10.0.0.21"
textport = 2004
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = int(textport)
server_address = (host, port)

#arduino setup
ser = serial.Serial('/dev/ttyACM0', 9600)                    

while 1 :
    str = ser.readline()
    str = str.decode("utf-8")
    soil, rain = str.split(":")
    print(soil)
    print(rain)
    soil = float(soil)
    rain = float(rain)
    
    if d1.isRaining(rain):
      #send udp message
      print("raining")
      data = "RainLimPassed"
      s.sendto(data.encode('utf-8'), server_address)
    elif (not d1.isRaining(rain)) and (d1.isDry(soil)):
      #send opposite message
      print("not raining")
      data = "ManualOpen"
      s.sendto(data.encode('utf-8'), server_address)
#    if d1.isDry(soil):
 #     #send udp message
      #define isdry
  #    print("soil is dry af")
   #   data = "ManualOpen"
    #  s.sendto(data.encode('utf-8'), server_address)
    elif not d1.isDry(soil):
      #send close message
      print("soil is moist")
      data = "MoistureLimPassed"
      s.sendto(data.encode('utf-8'), server_address)