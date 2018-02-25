import RPi.GPIO as GPIO
import time

#Set GPIO modes
GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)

LED1 = 23
LED2 = 24
LED3 = 12
LED4 = 16
LED5 = 20
LED6 = 21

#Need two constants, one to save the LED's current state and the other to save the switch's
led_state = 1

while True:
  #Check if the button was pressed
  time.sleep(.1)
  if led_state == 1:
    #Set the LED's in correspondance to the state
    GPIO.output(LED1, False)
    GPIO.output(LED2, False)
    GPIO.output(LED3, True)
    GPIO.output(LED4, True)
    GPIO.output(LED5, False)
    GPIO.output(LED6, False)
    #Change the LED based on the old state
    led_state += 1
  elif led_state == 2:
    #Set the LED's in correspondance to the state
    GPIO.output(LED1, False)
    GPIO.output(LED2, True)
    GPIO.output(LED3, False)
    GPIO.output(LED4, False)
    GPIO.output(LED5, True)
    GPIO.output(LED6, False)
    #Change the LED based on the old state
    led_state += 1
  elif led_state == 3:
    #Set the LED's in correspondance to the state
    GPIO.output(LED1, True)
    GPIO.output(LED2, False)
    GPIO.output(LED3, False)
    GPIO.output(LED4, False)
    GPIO.output(LED5, False)
    GPIO.output(LED6, True)
    #Change the LED based on the old state
    led_state += 1
  elif led_state == 4:
    #Set the LED's in correspondance to the state
    GPIO.output(LED1, False)
    GPIO.output(LED2, False)
    GPIO.output(LED3, False)
    GPIO.output(LED4, False)
    GPIO.output(LED5, False)
    GPIO.output(LED6, False)
    #Change the LED based on the old state
    led_state = 1
  #Reset the state of the switch after it's released
GPIO.cleanup()
