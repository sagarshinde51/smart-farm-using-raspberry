import RPi.GPIO as GPIO                    
import time                                
import urllib
import RPi.GPIO as GPIO
import dht11
import time
import datetime
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
GPIO.setmode(GPIO.BCM)

TRIG =  5 # board 3                                
ECHO = 6  # board 5                              
CLK  = 18 # board 12
MISO = 23  # board 16
MOSI = 24 # board 18
CS   = 25 # board 22
fan = 17 # board 11 for exost fan
motor = 27 #board 13 for water pump motor

GPIO.setup(fan,GPIO.OUT)     
GPIO.setup(motor,GPIO.OUT)     
GPIO.setup(TRIG,GPIO.OUT)                  
GPIO.setup(ECHO,GPIO.IN)                   
GPIO.setup(22,GPIO.OUT)
#GPIO.cleanup()
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)
# read data using pin 14
instance = dht11.DHT11(pin=14)
data= urllib.urlopen("https://api.thingspeak.com/update?api_key=YOA7OE17L85ZQTN&field1=0")//replace with your API
data1= urllib.urlopen("https://api.thingspeak.com/update?api_key=YOA7OE17L8HZQTN&field2=0")//replace with your API
data2= urllib.urlopen("https://api.thingspeak.com/update?api_key=YOA7OE17L85ZQTN&field3=0")//replace with your API

while True:
  result = instance.read()
  value = mcp.read_adc(1)
  moi = mcp.read_adc(2)
  light = mcp.read_adc(3)
  if result.is_valid():
    print("Last valid input: " + str(datetime.datetime.now()))
    print("Temperature: %d C" % result.temperature)
    print("Humidity: %d %%" % result.humidity)
    print("Moister level is: %d " %  value)
    result.temperature= urllib.urlopen("https://api.thingspeak.com/update?api_key=YOA7OE17L85HZQTN&field1="+str(result.temperature));
    result.humidity= urllib.urlopen("https://api.thingspeak.com/update?api_key=YOA7OE17L85HZQTN&field2="+str(result.humidity));
    moi= urllib.urlopen("https://api.thingspeak.com/update?api_key=YOA7OE17L85HZQTN&field3="+str(moi));
    light= urllib.urlopen("https://api.thingspeak.com/update?api_key=YOA7OE17L85HZQTN&field4="+str(light));


    if(result.temperature < 25):
      GPIO.output(fan, 0)
    if(value < 500):
      GPIO.output(motor, 0)

  GPIO.setup(TRIG,GPIO.OUT)                  
  GPIO.setup(ECHO,GPIO.IN)                   

  GPIO.output(TRIG, False)                 
 
  time.sleep(2)                            

  GPIO.output(TRIG, True)                  
  time.sleep(0.00001)                      
  GPIO.output(TRIG, False)                 

  while GPIO.input(ECHO)==0:               
    p_start = time.time()           

  while GPIO.input(ECHO)==1:               
    p_end = time.time()                

  p_duration = p_end - p_start 

  distance = p_duration * 17150        #Multiply pulse duration by 17150 to get distance
  distance = round(distance, 2)            #Round to two decimal points
  print "Distance:",distance ,"cm"  
  if distance < 10:
    GPIO.output(22, 1)
    time.sleep(0.1)
      
  else:
    time.sleep(1)
    GPIO.output(22, 0)
