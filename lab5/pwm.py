import RPi.GPIO as GPIO # Import the GPIO library.
import time # Import time library

GPIO.setmode(GPIO.BCM) # Use BCM numbes
GPIO.setup(18, GPIO.OUT) # Set GPIO 18 to output mode.

pwm = GPIO.PWM(18, 500) # Initialize PWM to a frequency of 500Hz
dutyCycle = 0
pwm.start(dutyCycle) # Start PWM with 0% duty cycle

while dutyCycle >= 0 and dutyCycle <=100:
 dutyCycle = int(input('Enter a PWM duty cycle (enter -1 to end): '))
 if dutyCycle == -1:
  break
 pwm.ChangeDutyCycle(dutyCycle)
 print("Duty cycle=",dutyCycle,'%')

pwm.stop()
GPIO.cleanup() # reset GPIO ports
