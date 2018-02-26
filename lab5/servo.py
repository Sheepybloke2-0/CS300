import RPi.GPIO as GPIO # Import the GPIO library.
import time # Import time library

GPIO.setmode(GPIO.BCM) # Use BCM numbers
GPIO.setup(18, GPIO.OUT) # Set GPIO 18 to output mode.

pwm = GPIO.PWM(18, 50) # Initialize PWM to a frequency of 50Hz
pwm.start(7.5)

try:
 while True:
  pwm.ChangeDutyCycle(7.5) # turn 90 degrees
  time.sleep(1) # wait for 1 second
  pwm.ChangeDutyCycle(2.5) # turn 0 degrees
  time.sleep(1) # wait for 1 second
  pwm.ChangeDutyCycle(12.5) # turn 180 degrees
  time.sleep(1) # wait for 1 second
except KeyboardInterrupt:
 pwm.stop() # stop the PWM signal
 GPIO.cleanup()
