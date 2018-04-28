import paho.mqtt.client as mqtt
import Adafruit_MCP9808.MCP9808 as MCP9808
import RPi.GPIO as GPIO
import time

# ------ Globals -------------
BROKER = "iot.cs.calvin.edu"
PORT = 1883
QOS = 0

# Number of seconds between temp loging. For demo use 10s
TEMP_LOG_TIME = 2

# GPIO pins
ROLLER_SW = 23
RESET_BTN = 25

# Number of cans in the system. Updated through MQTT.
num_cans = 12
current_cans = num_cans


def c_to_f(c):
        return c * 9.0 / 5.0 + 32.0


def publish_can_count(cans):
    result, num = mqtt_client.publish("rtl5/cur_cans", cans, QOS)
    if result != 0:
        print("ERROR: Can count PUBLISH failed")
    print('Current cans ' + str(cans))


def update_can_count(channel):
    global current_cans
    if current_cans != 0:
        current_cans -= 1
    else:
        current_cans = 0

    publish_can_count(current_cans)


def reset_can_count(channel):
    global current_cans
    current_cans = num_cans
    publish_can_count(current_cans)


def send_temp():
    temp = temp_sensor.readTempC()
    temp_msg = c_to_f(temp)
    time_local = time.localtime()
    time_msg = str(time_local.tm_hour) + ':' + str(time_local.tm_min) + '.' + str(time_local.tm_sec)

    result, num = mqtt_client.publish("rtl5/temp", temp_msg, QOS)
    if result != 0:
        print("ERROR: Temp PUBLISH failed with "  + str(result))

    result, num = mqtt_client.publish("rtl5/time", time_msg, QOS)
    if result != 0:
        print("ERROR: Time PUBLISH failed with "  + str(result))

    print('Temp ' + str(temp_msg) +  ' F at ' + time_msg)
    time.sleep(TEMP_LOG_TIME)


def on_connect(client, userdata, rc, *extra_params):
    print("Connection to " + BROKER + " with result code !" + str(rc))


def on_can_nmb_msg(client, data, msg):
    global num_cans
    if msg.topic == "rtl5/num_cans":
        num_cans = int(msg.payload)
        print(num_cans)


if __name__ == '__main__':
    # ------------ Setup --------------------
    GPIO.setmode(GPIO.BCM)
    # Set up the Buttons to start at 1
    GPIO.setup(ROLLER_SW, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(RESET_BTN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    temp_sensor = MCP9808.MCP9808()

    mqtt_client = mqtt.Client()
    mqtt_client.on_message = on_can_nmb_msg
    mqtt_client.on_connect = on_connect
    mqtt_client.connect(BROKER, PORT, 60)
    mqtt_client.subscribe('rtl5/num_cans', qos=QOS)
    mqtt_client.loop_start()

    GPIO.add_event_detect(ROLLER_SW, GPIO.RISING, callback=update_can_count, bouncetime=200)
    GPIO.add_event_detect(RESET_BTN, GPIO.RISING, callback=reset_can_count, bouncetime=200)

    while True:
        try:
            send_temp()
        except KeyboardInterrupt:
            break

    mqtt_client.disconnect()
