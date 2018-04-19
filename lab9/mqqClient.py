# CS300 Lab 9 MQTT client
import Adafruit_MCP9808.MCP9808 as MCP9808
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time

# Constants
BROKER = "iot.cs.calvin.edu"
PORT = 1883
QOS = 0
LED = 21

# Initialize GPIO and temperature sensor object
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT)
sensor = MCP9808.MCP9808()

# Callback when a message is published
def on_publish(client, userdata, mid):
 print("MQTT data published")

# Callback when a connection has been established with the MQTT broker
def on_connect(client, userdata, rc, *extra_params):
 print('Connected with result code='+str(rc))

# Callback when client receives a PUBLISH message from the broker
def on_message(client, data, msg):
 if msg.topic == "rtl5/LED":
  print("Received message: LED = ", int(msg.payload))
 if int(msg.payload) == 1:
  GPIO.output(LED, True)
 elif int(msg.payload) == 0:
  GPIO.output(LED, False)

# Setup MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish

# Connect to MQTT broker and subscribe to the button topic
client.connect(BROKER, PORT, 60)
client.subscribe("rtl5/LED", qos=QOS)
client.loop_start()

# Continuously publish temperature data till ctrl-C is hit
try:
 while True:
  # Read MCP9808 sensor and publish the reading
  temp = sensor.readTempC()
  client.publish("rtl5/temperature", temp)
  time.sleep(3)
  
except KeyboardInterrupt:
 print('Done')
 client.disconnect()
