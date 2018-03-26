import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)


GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)  #Button1
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)  #Button2
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)  #Button3
GPIO.setup(21, GPIO.OUT) #GLED
GPIO.setup(20, GPIO.OUT) #RLED
holder = [0,0,0,0]
pswd = [1,2,3,3]
state = 1
count = 0


def my_callback(channel):
    global state, holder, pswd, count
    # time.sleep(0.25)
    if count < 4:
        button1 = GPIO.input(23)
        # print("Button 1:", button1)
        button2 = GPIO.input(24)
        # print("Button 2:", button2)
        button3 = GPIO.input(16)
        # print("Button 3:", button3)
        if (button1 != 1 or button2 != 1 or button3 != 1):
            if state == 1:
                if button1 == 0:
                    holder[0] = 1
                elif button2 == 0:
                    holder[0] = 2
                elif button3 == 0:
                    holder[0] = 3
            elif state == 2:
                if button1 == 0:
                    holder[1] = 1
                elif button2 == 0:
                    holder[1] = 2
                elif button3 == 0:
                    holder[1] = 3
            elif state == 3:
                if button1 == 0:
                    holder[2] = 1
                elif button2 == 0:
                    holder[2] = 2
                elif button3 == 0:
                    holder[2] = 3
            elif state == 4:
                if button1 == 0:
                    holder[3] = 1
                elif button2 == 0:
                    holder[3] = 2
                elif button3 == 0:
                    holder[3] = 3
                if holder == pswd:
                    GPIO.output(21, True)
                    time.sleep(3)
                    GPIO.output(21, False)
                else:
                    GPIO.output(20, True)
                    time.sleep(3)
                    GPIO.output(20, False)
            state += 1
            count += 1

GPIO.add_event_detect(23, GPIO.FALLING, callback=my_callback, bouncetime = 200)
GPIO.add_event_detect(24, GPIO.FALLING, callback=my_callback, bouncetime = 200)
GPIO.add_event_detect(16, GPIO.FALLING, callback=my_callback, bouncetime = 200)

while True:
    if state == 5:
        print(holder)
        holder = [0, 0, 0, 0]
        state = 1
        count = 0


GPIO.cleanup()           # clean up GPIO on normal exit

