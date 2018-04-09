from flask import Flask, render_template
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
import pygal
import eventlet

eventlet.monkey_patch()

# ------ Globals -------------
BROKER = "iot.cs.calvin.edu"
PORT = 1883
REFRESH_TIME = 10 # seconds

TITLE = 'Temperature of Fridge over Time'

num_cans = 12
current_cans = num_cans
times_data =[0]
temp_data =[0]

async_mode = None

app = Flask(__name__)
# Configs for Flask app
app.config['SECRET'] = 'secretkey'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL']   = BROKER
app.config['MQTT_BROKER_PORT']  = PORT
app.config['MQTT_REFRESH_TIME'] = REFRESH_TIME

mqtt = Mqtt(app)
socketio = SocketIO(app, async_mode=async_mode)


# WebApp functions
@app.route('/')
def index():
    global times_data, temp_data
    line_chart = pygal.StackedLine(fill=True, title=TITLE,
                                   disable_xml_declaration=True)
    line_chart.x_labels = times_data
    line_chart.add('Temperature (F)', temp_data)
    return render_template('index.html', title="Welcome!", line_chart=line_chart)


# MQTT/Socketio functions
@socketio.on('update_can_number')
def handle_publish(json_str):
    data = json.loads(json_str)
    mqtt.publish(data['topic'], data['msg'])


@socketio.on('mqtt_messsage')
def handle_message(dict_msg):
    global times_data, temp_data, cur_cans
    data = dict_msg
    print(data['topic'], data['msg'])
    if data['topic'] is "rtl5/cur_cans":
        cur_cans = data['msg']

    if data['topic'] is "rtl5/time":
        cur_time = data['msg']
        if len(times_data) <= 50:
            times_data.append(cur_time)
        else:
            times_data[50] = cur_time

    if data['topic'] is "rtl5/temp":
        cur_temp = data['msg']
        if len(temp_data) <= 50:
            temp_data.append(cur_temp)
        else:
            temp_data[50] = cur_temp

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    print("Subscribing")
    mqtt.subscribe('rtl5/temp')
    mqtt.subscribe('rtl5/time')
    mqtt.subscribe('rtl5/num_cans')
    mqtt.subscribe('rtl5/cur_cans')


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    global times_data, temp_data, cur_cans
    data = dict(
         topic=message.topic,
         msg=message.payload.decode()
    )
    if data['topic'] == u'rtl5/cur_cans':
        cur_cans = data['msg']

    if data['topic'] == u'rtl5/time':
        cur_time = data['msg']
        if len(times_data) <= 50:
            times_data.append(cur_time)
        else:
            times_data[50] = cur_time

    if data['topic'] == u'rtl5/temp':
        cur_temp = data['msg']
        if len(temp_data) <= 50:
            temp_data.append(float(cur_temp))
        else:
            temp_data[50] = float(cur_temp)
        socketio.emit('handle_messsage', data, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True)
