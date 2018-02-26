import RPi.GPIO as GPIO # Import the GPIO library.
import time # Import time library

GPIO.setmode(GPIO.BCM) # Use BCM numbers
GPIO.setup(18, GPIO.OUT) # Set GPIO 18 to output mode.

pwm = GPIO.PWM(18, 50) # Initialize PWM to a frequency of 50Hz
pwm.start(7.5)
t = 0.001
add = True

try:
 while True:
  dt = (t / 0.02)*100
  pwm.ChangeDutyCycle(dt) # turn 90 degrees
  time.sleep(0.1) # wait for 1 second
  print(dt)
  
  if add is True:
   t += 0.0001
  else:
   t -= 0.0001
  if dt >= 11.5:
   add = False
  if dt <= 2.5:
   add = True

except KeyboardInterrupt:
 pwm.stop() # stop the PWM signal
 GPIO.cleanup()
