import RPi.GPIO as GPIO # Import the GPIO library.
import time # Import time library

GPIO.setmode(GPIO.BCM) # Use BCM numbes
GPIO.setup(18, GPIO.OUT) # Set GPIO 18 to output mode.

pwm = GPIO.PWM(18, 500) # Initialize PWM to a frequency of 500Hz
dutyCycle = 0
pwm.start(dutyCycle) # Start PWM with 0% duty cycle
add = True
end = 0

while(True):

 if add is True:
  dutyCycle += 1
 else:
  dutyCycle -= 1

 pwm.ChangeDutyCycle(dutyCycle)
 print("Duty cycle=",dutyCycle,'%')
 
 if dutyCycle >= 100:
  add = False

 if dutyCycle <= 0:
  add = True
  end += 1

 time.sleep(0.1)
 if end >= 5:
  break

pwm.stop()
GPIO.cleanup() # reset GPIO ports
