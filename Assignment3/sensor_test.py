import Adafruit_MCP9808.MCP9808 as MCP9808
from time import sleep
# Create temperature sensor object
sensor = MCP9808.MCP9808()
# Continuously take temperature samples till ctrl-C is hit
try:
 while True:
  # Read MCP9808 sensor
  temp = sensor.readTempC()
  print("Temperature:", temp,"degrees C")
  sleep(1)
except KeyboardInterrupt:
 print('Done')
