import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt

GPIO.setmode(GPIO.BCM)
SCL = 3
SDA = 2
icAddress = 0x18
registerAddress = 0x05

# Constants
BROKER = "iot.cs.calvin.edu"
PORT = 1883
QOS = 0

icAddress = bin(icAddress)[2:]
icAddress = icAddress.zfill(7)
icAddress = [int(x) for x in icAddress]
icAddress.append(0)

registerAddress = bin(registerAddress)[2:]
registerAddress = registerAddress.zfill(8)
registerAddress = [int(x) for x in registerAddress]


def getTemperature():
    #Local Constants
    global SCL, SDA, icAddress, registerAddress
    GPIO.setup(SCL, GPIO.OUT)
    sendStart()
   
    #Write icAddress w/ WRITE Bit
    icAddress[7] = 0
    if(writeData(icAddress) == False):
        print("Address not Acknowledged by Sensor for initial write !!")
    
    if(writeData(registerAddress) == False):
        print("Register not Acknowledged by Sensor!!")

    sendStart()

    #Change R/W bit to Read
    icAddress[7] = 1
    if(writeData(icAddress) == False):
        print("Address not Acknowledged by Sensor for Data Read !!")
    
    msbData = readData()
    sendACK()
    lsbData = readData()
    sendNAK()
    sendStop()

    #Convert the binary list into a number and clear flags
    UpperByte = ''.join(str(x) for x in msbData)
    UpperByte = int(hex(int(UpperByte, 2))[2:] , 16)
    UpperByte = UpperByte & 0x1F

    LowerByte = ''.join(str(x) for x in lsbData)
    LowerByte = int(hex(int(LowerByte, 2))[2:] , 16)

    if ((UpperByte & 0x10) == 0x10):
        UpperByte = UpperByte & 0x0F
        Temperature = 256 - (UpperByte * 16 + LowerByte / 16)
    else:
        Temperature = (UpperByte * 16 + LowerByte / 16)
    print("Temperature in Celsius: ", Temperature)
    return Temperature

#Start Sequence
def sendStart():
    global SCL, SDA, icAddress
    GPIO.setup(SDA, GPIO.OUT)
    GPIO.output(SDA, True)
    GPIO.output(SCL, True)
    time.sleep(0.001)
    GPIO.output(SDA, False)
    time.sleep(0.001)
    GPIO.output(SCL, False)

def writeData(data):
    global SCL, SDA, icAddress
    GPIO.setup(SDA, GPIO.OUT)
    for i in range(0,len(data)):
        GPIO.output(SDA, data[i])
        time.sleep(0.001)
        GPIO.output(SCL, True)
        time.sleep(0.001)
        GPIO.output(SCL, False)
        time.sleep(0.001)

    #Check ACK
    GPIO.setup(SDA, GPIO.IN)
    GPIO.output(SCL, True)
    time.sleep(0.001)
    ackNak = GPIO.input(SDA)
    GPIO.output(SCL, False)
    if ackNak == True:
        return False
    else:
        return True

def readData():
    GPIO.setup(SDA, GPIO.IN)
    readByte = []
    for bit in range(0, 8):
        GPIO.output(SCL, True)
        time.sleep(0.001)
        readByte.append(GPIO.input(SDA))
        GPIO.output(SCL, False)
        time.sleep(0.001)
    return readByte

def sendACK():
    GPIO.setup(SDA, GPIO.OUT)
    GPIO.output(SDA, False)
    time.sleep(0.001)
    GPIO.output(SCL, True)
    time.sleep(0.001)
    GPIO.output(SCL, False)
    time.sleep(0.001)

def sendNAK():
    GPIO.setup(SDA, GPIO.OUT)
    GPIO.output(SDA, True)
    time.sleep(0.001)
    GPIO.output(SCL, True)
    time.sleep(0.001)
    GPIO.output(SCL, False)
    time.sleep(0.001)

def sendStop():
    global SCL, SDA, icAddress
    GPIO.setup(SDA, GPIO.OUT)
    GPIO.output(SDA, False)
    time.sleep(0.001)
    GPIO.output(SCL, True)
    time.sleep(0.001)
    GPIO.output(SDA, True)
    time.sleep(0.001)
    GPIO.output(SCL, False)

# Callback when a message is published
def on_publish(client, userdata, mid):
 print("data published")

# Callback when a connection has been established with the MQTT broker
def on_connect(client, userdata, rc, *extra_params):
 print('Connected with result code='+str(rc))

if __name__ == '__main__':
 # Setup MQTT client
 client = mqtt.Client()
 client.on_connect = on_connect
 client.on_publish = on_publish

 # Connect to MQTT broker and subscribe to the button topic
 client.connect(BROKER, PORT, 60)

 while (True):
  try:
   message = getTemperature()
   # Publish message to broker
   (result, num) = client.publish("dwm5/temperature", message, qos=0, retain=True)
   if result != 0:
    print("PUBLISH returned error:", result)
     
   time.sleep(2)

  except KeyboardInterrupt:
    break

 client.disconnect()

 GPIO.cleanup()
