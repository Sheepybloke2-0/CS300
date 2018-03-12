# CS300 Lab 7 MQTT client
import paho.mqtt.client as mqtt

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
 if msg.topic == "adr22/button":
  print("button = " + str(int(msg.payload)))

# Setup MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish

# Connect to MQTT broker and subscribe to the button topic
client.connect(BROKER, PORT, 60)
client.subscribe("adr22/button", qos=QOS)
client.loop_start()

while True:
 print("1) turn on LED1")
 print("2) turn off LED1")
 print("3) quit")
 selection = input("Enter your selection: ")
 if selection == "1":
  message = 1
 elif selection == "2":
  message = 0
 elif selection == "3":
  break
 else:
  continue

 # Publish message to broker
 (result, num) = client.publish("rtl5/LED", message, qos=0)
 if result != 0:
  print("PUBLISH returned error:", result)
client.disconnect()
