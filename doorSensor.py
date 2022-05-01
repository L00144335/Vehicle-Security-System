import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM) # allows to reference RPi GPIO Pins using numbers
GPIO.setwarnings(False) # remove channel warnings

DOOR = 25

GPIO.setup(DOOR, GPIO.OUT) # door

while True:
	while GPIO.input(DOOR) == 0 :
		print("The Door is closed")
		#time.sleep(2)
	
	
	while GPIO.input(DOOR) == 1 :
		print("The Door is open")
		#time.sleep(2)
