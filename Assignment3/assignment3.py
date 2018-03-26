def getTemperature():
    import RPi.GPIO as GPIO
    import time
    GPIO.setmode(GPIO.BCM)
    address = []
    GPIO.setup(3, GPIO.OUT) #SCL

    #Start Sequence
    GPIO.setup(2, GPIO.OUT)
    GPIO.output(3, True)
    GPIO.output(2, True)
    time.sleep(0.001)
    GPIO.output(2, False)
    time.sleep(0.001)
    GPIO.output(3, False)
