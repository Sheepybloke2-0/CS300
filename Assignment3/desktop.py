import paho.mqtt.client as mqtt

# ------ Globals -------------
BROKER = "iot.cs.calvin.edu"
PORT = 1883
QOS = 0
TOPIC = 'dwm5/temperature'

temp = 0

# ------ Functions -------------
def c_to_f(c):
    return c * 9.0 / 5.0 + 32.0


def on_connect(client, userdata, rc, *extra_params):
    print("Connection to " + BROKER + " with result code !" + str(rc))


def on_temp_msg(client, data, msg):
    global temp
    if msg.topic == TOPIC:
        temp = msg.payload

if __name__ == '__main__':
    mqtt_client = mqtt.Client()
    mqtt_client.on_message = on_temp_msg
    mqtt_client.on_connect = on_connect
    mqtt_client.connect(BROKER, PORT, 60)
    mqtt_client.loop_start()
    mqtt_client.subscribe(TOPIC, qos=QOS)

    old_temp = 0
    print('Getting the temp from pi!')
    while True:
        try:
            if temp != old_temp:
                print('The current temperature is %s C, or %s F' % (temp, c_to_f(float(temp))))
                old_temp = temp

        except KeyboardInterrupt:
            break

    mqtt_client.disconnect()
