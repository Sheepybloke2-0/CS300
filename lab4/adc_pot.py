from time import sleep
import Adafruit_MCP3008

# Create MCP3008 object using specified pin numbers:
a2d = Adafruit_MCP3008.MCP3008(clk=18, cs=25, miso=23, mosi=24)

print('Press Ctrl-C to quit...')

while True:
 a2d0 = a2d.read_adc(0)
 print('A/D input channel 0 = ', a2d0)
 sleep(0.5)
