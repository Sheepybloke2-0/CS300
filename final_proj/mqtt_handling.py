'''
CS 300 Final Project: Can Counter
By Dan Michaels and Reuben Lewis
mqtt_handling.py:
A short Python program handling the counting of the number of cans in a rack
and transfering the data over MQTT to a webpage.
'''
import paho.mqtt.client as mqtt
import Adafruit_MCP9808.MCP9808 as MCP9808
import RPi.GPIO as GPIO
import time

# ------ Globals -------------
# MQTT constants
BROKER = "iot.cs.calvin.edu"
PORT   = 1883
QOS    = 0

# Number of seconds between temp loging. For demo use 10s
TEMP_LOG_TIME = 10

# GPIO pins
PUSH_BTN  = 23
RESET_BTN = 25

# Total number of cans in the system. Updated through MQTT.
total_cans = 12

# The current number of cans in the system.
current_cans = total_cans


def c_to_f(c):
    '''
    Convert the temperature gotten from the sensor in Celcius to Fahrenheit.
    '''
    return c * 9.0 / 5.0 + 32.0


def publish_total_cans():
    '''
    Publish the total number of cans to the MQTT broker.
    '''
    global total_cans
    result, num = mqtt_client.publish("rtl5/total_cans", total_cans, QOS)
    if result != 0:
        print("ERROR: Can count PUBLISH failed")
    print('Total number of cans is ' + str(total_cans))


def publish_can_count(cans):
    '''
    Publish the current number of cans to the MQTT broker.
    '''
    result, num = mqtt_client.publish("rtl5/cur_cans", cans, QOS)
    if result != 0:
        print("ERROR: Can count PUBLISH failed")
    print('Current cans ' + str(cans))


def update_can_count(channel):
    '''
    Callback function for click event of the PUSH_BTN. Decrement the current cans
    by 1 and ensure that they don't go negative, then publish the count.
    '''
    global current_cans
    if current_cans != 0:
        current_cans -= 1
    else:
        current_cans = 0

    publish_can_count(current_cans)


def reset_can_count(channel):
    '''
    Callback frunction for the reset button. Set the current number of cans to
    the total number of cans, then publish the data.
    '''
    global current_cans
    current_cans = total_cans
    publish_can_count(current_cans)


def send_temp():
    '''
    Read the temperature sensor, and publish it along with the current time after
    converting the temp to Fahrenheit.
    '''
    temp = temp_sensor.readTempC()
    temp_fahr = c_to_f(temp)
    time_local = time.localtime()
    time_msg = str(time_local.tm_hour) + ':' + str(time_local.tm_min) + '.' + str(time_local.tm_sec)

    result, num = mqtt_client.publish("rtl5/temp", temp_fahr, QOS)
    if result != 0:
        print("ERROR: Temp PUBLISH failed with "  + str(result))

    result, num = mqtt_client.publish("rtl5/time", time_msg, QOS)
    if result != 0:
        print("ERROR: Time PUBLISH failed with "  + str(result))

    print('Temp ' + str(temp_msg) +  ' F at ' + time_msg)


def on_connect(client, userdata, rc, *extra_params):
    '''
    Print a confirmation on connect.
    '''
    print("Connection to " + BROKER + " with result code !" + str(rc))


def on_message(client, data, msg):
    '''
    Two messages can be recieved: the total_cans topic, which updates the total
    number of cans as sent from the webpage, and the status topic, which is sent
    when a webpage is opened. This causes the current and total number of cans to
    be sent to the webpage, causing it to be updated.
    '''
    global total_cans
    global current_cans
    if msg.topic == "rtl5/total_cans":
        total_cans = int(msg.payload)
        print(total_cans)
    elif msg.topic == "rtl5/status":
        # Message payloads are in byte format, so compare with a byte type string.
        if msg.payload == b'Connected':
            print("A client has connected")
            publish_can_count(current_cans)
            publish_total_cans()

if __name__ == '__main__':
    # ------------ Setup --------------------
    GPIO.setmode(GPIO.BCM)
    # Set up the Buttons to start at 1
    GPIO.setup(PUSH_BTN GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(RESET_BTN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    temp_sensor = MCP9808.MCP9808()

    mqtt_client = mqtt.Client()
    mqtt_client.on_message = on_message
    mqtt_client.on_connect = on_connect
    mqtt_client.connect(BROKER, PORT, 60)
    mqtt_client.subscribe('rtl5/total_cans', qos=QOS)
    mqtt_client.subscribe('rtl5/status', qos=QOS)
    mqtt_client.loop_start()

    GPIO.add_event_detect(ROLLER_SW, GPIO.RISING, callback=update_can_count, bouncetime=200)
    GPIO.add_event_detect(RESET_BTN, GPIO.RISING, callback=reset_can_count, bouncetime=200)

    while True:
        try:
            send_temp()
        except KeyboardInterrupt:
            break
        # After sending the temp, wait to read again. This doesn't affect the callback functions.
        time.sleep(TEMP_LOG_TIME)

    mqtt_client.disconnect()
