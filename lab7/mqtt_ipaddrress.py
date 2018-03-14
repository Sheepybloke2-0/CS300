# CS300 Lab 7 MQTT client
import paho.mqtt.client as mqtt
import time

# Constants
BROKER = "iot.cs.calvin.edu"
PORT = 1883
QOS = 0

# Callback when a message is published
def on_publish(client, userdata, mid):
 print("data published")

# Callback when a connection has been established with the MQTT broker
def on_connect(client, userdata, rc, *extra_params):
 print('Connected with result code='+str(rc))

# Callback when client receives a PUBLISH message from the broker
def on_message(client, data, msg):
 if msg.topic == "rtl5/ipaddress":
  print("My IP address is:   " + str(msg.payload))

# Setup MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish

# Connect to MQTT broker and subscribe to the button topic
client.connect(BROKER, PORT, 60)
client.subscribe("rtl5/ipaddress", qos=QOS)
client.loop_start()

time.sleep(10)

client.disconnect()
