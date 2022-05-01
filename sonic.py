#!/usr/bin/env python3
# import the necessary libraries
import RPi.GPIO as GPIO
import time, atexit
from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD

GPIO.setmode(GPIO.BCM) # allows to reference RPi GPIO Pins using numbers

# used refresh the display
def safe_exit(signum, frame):
	exit(1)

# declare objects (pins) and assign numbers
lcd = LCD()
LED_PIN = 17
TRIG = 23
ECHO = 24
DOOR = 25
print("Distance measurement in progress")
# set up gpio pins
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(DOOR, GPIO.OUT)
signal(SIGTERM, safe_exit)
signal(SIGHUP, safe_exit)

GPIO.output(TRIG, False)
print("Waiting for sensor to settle")
time.sleep(2)

# main loop
while True:
    GPIO.output(TRIG, True) # send wave
    time.sleep(0.00001)
    GPIO.output(TRIG, False) # settle
    
    # try door sensor here
    #if GPIO.input(DOOR) == 0 :
     #   print("Closed")
    #if GPIO.input(DOOR) == 1 :
     #   print("Open")

    while GPIO.input(ECHO) == 0: # pulse
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time() # read when pulse is back

    pulse_duration = pulse_end - pulse_start # calculate pulse duration
    distance = pulse_duration * 17150 # measure distance based on duration
    distance = round(distance, 2) # round distance to 2 decimals
    print("Distance", distance, "cm")
    #message = "Distance " + str(distance) # set up message (cast float to string)
    #lcd.text(message, 1) # display message to LCD every 2 seconds
    #time.sleep(2)
    
    if distance < 85.00 : # if the distance is below 46cm
        GPIO.output(LED_PIN, GPIO.HIGH) # LED on
        lcd.text("Intruder Detected", 3) # message Intruder Detected
    else :
        GPIO.output(LED_PIN, GPIO.LOW) 
        lcd.text("",3)


def exit_nadler():
    ldc.clear()
    GPIO.cleanup()

atexit.register(exit_handler)
