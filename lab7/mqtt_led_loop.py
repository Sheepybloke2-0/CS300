# CS300 Lab 7 MQTT client
import paho.mqtt.client as mqtt
import time

# Constants
BROKER = "iot.cs.calvin.edu"
PORT = 1883
QOS = 0

message = 1
break = 0

# Callback when a message is published
def on_publish(client, userdata, mid):
 print("data published")

# Callback when a connection has been established with the MQTT broker
def on_connect(client, userdata, rc, *extra_params):
 print('Connected with result code='+str(rc))

# Callback when client receives a PUBLISH message from the broker
def on_message(client, data, msg):
 global break
 if msg.topic == "rtl5/button":
  break = 1
  return break
 else:
  break = 0
  return break

# Setup MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish

# Connect to MQTT broker and subscribe to the button topic
client.connect(BROKER, PORT, 60)
client.subscribe("rtl5/button", qos=QOS)
client.loop_start()


while (break == 0):
  # Publish message to broker
 (result, num) = client.publish("rtl5/LED", message, qos=0)
 if result != 0:
  print("PUBLISH returned error:", result)
 if (message == 0):
  message = 1
 else:
  message = 0

 time.sleep(1)

client.disconnect()
