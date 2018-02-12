import RPi.GPIO as GPIO

#Set GPIO modes
GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(16, GPIO.OUT)

#Need two constants, one to save the LED's current state and the other to save the switch's
led_state = 1
switch_state = 1

while True:
  #Check if the button was pressed
  if GPIO.input(12) == False and switch_state == 0:
    #Set the state to pressed so that holding the button down doesn't keep switching the LED
    switch_state = 1
    #Change the LED based on the old state
    if led_state == 1:
      GPIO.output(16, False)
      led_state = 0
    else:
      GPIO.output(16, True)
      led_state = 1
  #Reset the state of the switch after it's released
  if GPIO.input(12) == True and switch_state == 1:
    switch_state = 0

