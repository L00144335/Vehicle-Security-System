# Vehicle Security System v0.1
# Current features
	# door sensor +
	# ultrasonic sensor +
	# LCD messages +
	# Face Recognition +
	# Email notifications +
	# Firebase Upload +

# import the necessary libraries
import RPi.GPIO as GPIO # control GPIO pins (receive input/output)
import time, atexit     # used to past time and cleat LCD when program ends
from signal import signal, SIGTERM, SIGHUP, pause # needed to control LCD
from rpi_lcd import LCD # main LCD library

# libraries and packaged required for Face Recognition
from imutils.video import VideoStream # image processing vor video stream
from imutils.video import FPS # image processing to set FPS and improve performance
import face_recognition # Python's face_recognition library (dlib features) 
import imutils # Main imutils for image processing
import pickle # Used to serialize and deserialize objecs (e.g., image arrays)
import cv2 # OpenCV Library

# Email imports
from Emailer import Emailer

# Firebase imports (date to avoid image overwrite)
from Firebase import Firebase
from datetime import datetime

# get the current time
now = datetime.now()
current_time = now.strftime("%H:%M:%S")



# Enable BCM mode to allow objects to reference number pins on RPi
GPIO.setmode(GPIO.BCM) # allows to reference RPi GPIO Pins using numbers
GPIO.setwarnings(False) # remove channel warnings

# Declare the required pins as objects
# declare objects (pins) and assign numbers
lcd = LCD() # LCD object
LED_PIN = 17 # LED this won't be used for the final version
TRIG = 23 # send out a sonic wave
ECHO = 24 # settle wave
DOOR = 25 # door sensor


# declare class object and set up subject and content and receiver
sender = Emailer()
sendTo = 'mrkostadinov7@gmail.com'
emailSubject = "INTRUDER DETECTED" #The Subject of the Email
emailContent = "Someone is trying to steal your car photograph below"

# declare object for Firebase
fireCloud = Firebase()

# define safe_exit for LCD
def safe_exit(signum, frame):
	exit(1)

# set up variables for face recognition
ownername = "Unknown" # set initially to unknown
# Get encodings.pickle file model created from train_model.py to try and match with
# the current video stream
encodingsP = "encodings.pickle"

# store the owner's face using pickle to load the cascade (Haar + images)
data = pickle.loads(open(encodingsP, "rb").read())

# Enable GPIO pins
# set up gpio pins
GPIO.setup(TRIG, GPIO.OUT) # sonic (send wave)
GPIO.setup(ECHO, GPIO.IN) # sonic (detect when wave is back)
GPIO.setup(LED_PIN, GPIO.OUT) # LED
GPIO.setup(DOOR, GPIO.OUT) # door
signal(SIGTERM, safe_exit) # LCD
signal(SIGHUP, safe_exit) # LCD



# Part 1 - need to detect when the vehicle door is open and take actions
# based on that.

# main loop to ensure that the program runs continuously
while True:
	# While the door is closed do nothing
	while GPIO.input(DOOR) == 0 :
		print("Door is closed")
		lcd.text("Door is closed", 1)
		time.sleep(2)
	
	# If the door opens try to detect a person
	while GPIO.input(DOOR) == 1 :
		lcd.text("Door is open", 1)
		
		# initiate ultrasonic
		GPIO.output(TRIG, True) # send wave
		time.sleep(0.00001)
		GPIO.output(TRIG, False) # settle
		
		while GPIO.input(ECHO) == 0: # pulse
			pulse_start = time.time()

		while GPIO.input(ECHO) == 1:
			pulse_end = time.time() # read when pulse is back
			
		# detect person here and calculate pulse duration in centimeters		
		pulse_duration = pulse_end - pulse_start # calculate pulse duration
		distance = pulse_duration * 17150 # measure distance based on duration
		distance = round(distance, 2) # round distance to 2 decimals
		print("Distance", distance, "cm")
		#message = "Distance " + str(distance) # set up message (cast float to string)
		#lcd.text(message, 1) # display message to LCD every 2 seconds
		#time.sleep(1)
    
		if distance < 85.00 : # if the distance is below 85cm
			print("Waiting to detect again")
			time.sleep(5)
			
			# ultrasonic again
			# initiate ultrasonic
			GPIO.output(TRIG, True) # send wave
			time.sleep(0.00001)
			GPIO.output(TRIG, False) # settle
		
			while GPIO.input(ECHO) == 0: # pulse
				pulse_start = time.time()

			while GPIO.input(ECHO) == 1:
				pulse_end = time.time() # read when pulse is back
			
			# detect person here and calculate pulse duration in centimeters		
			pulse_duration = pulse_end - pulse_start # calculate pulse duration
			distance = pulse_duration * 17150 # measure distance based on duration
			distance = round(distance, 2) # round distance to 2 decimals
			print("Distance", distance, "cm")
			
			if distance < 85.00 : # now surely someone is in the car seat
				#GPIO.output(LED_PIN, GPIO.HIGH) # LED on
				lcd.text("Intruder Detected", 1) # message Intruder Detected
			
			
				# initiate face recognition
				# warm up the camera
				vs = VideoStream(usePiCamera=True).start()
				time.sleep(2.0)

				# start the FPS counter
				fps = FPS().start()
			
				# check how long it take to identify the owner here
				start = time.time()
			
				while True:
					# grab the frame from the threaded video stream and resize it
					# to 500px (to speedup processing)
					frame = vs.read()
					frame = imutils.resize(frame, width=500)
					# Detect face boxes using face_recognition
					boxes = face_recognition.face_locations(frame)
					# compute the facial embeddings for each face bounding box
					encodings = face_recognition.face_encodings(frame, boxes)
					# store names (in this case it will be only one)
					names = []
				
					# loop over the facial embeddings
					for encoding in encodings:
						# attempt to match each face in the input image to our known
						# encodings
						matches = face_recognition.compare_faces(data["encodings"],
						encoding)
						name = "Unknown" # set name to unknown if not recognised

						# check to see if we have found a match
						if True in matches:
							# find the indexes of all matched faces then initialize a
							# dictionary to count the total number of times each face
							# was matched
							matchedIdxs = [i for (i, b) in enumerate(matches) if b]
							counts = {}
						
						
							# loop over the matched indexes and maintain a count for
							# each recognized face face
							for i in matchedIdxs:
								name = data["names"][i]
								counts[name] = counts.get(name, 0) + 1

							# determine the recognized face with the largest number
							# of votes (note: in the event of an unlikely tie Python
							# will select first entry in the dictionary)
							name = max(counts, key=counts.get)

							#If someone in your dataset is identified, print their name on the screen
							if ownername != name:
								ownername = name
								print(ownername)
							
						# update the list of names
						names.append(name)
				
					# loop over the recognized faces
					for ((top, right, bottom, left), name) in zip(boxes, names):
						# draw the predicted face name on the image - color is in BGR
						cv2.rectangle(frame, (left, top), (right, bottom),
							(0, 255, 225), 2)
						y = top - 15 if top - 15 > 15 else top + 15
						cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
							.8, (0, 255, 255), 2)
						
					# show frame
					# display the image to our screen
					cv2.imshow("Facial Recognition in Progress", frame)
					key = cv2.waitKey(1) & 0xFF
				
					if ownername == "Mario":
						lcd.text("Owner Recognised", 1)
						lcd.text("Engine OK", 2)
						lcd.text("Permission to drive", 3)
						print("Owner Recognised")
						print("Engine OK")
						print("Permission to drive")
						# print time here
						stop = time.time()
						print("Time to recognise= ", round(stop - start, 2), "seconds")
					
						# close frames and terminate the program
						fps.update()
						fps.stop()
						cv2.destroyAllWindows()
						vs.stop()
						exit()
						
						
					elif ownername == "Unknown" :
						lcd.text("Intruder detected", 1)
						lcd.text("Engine OFF", 2)
						lcd.text("Doors Locked", 3)
						print("Intruder detected")
						print("Engine OFF")
						print("Doors Locked")
					
						#email and photo starts here
						img_name = "intruder at "+current_time+".jpg" # give image name
						cv2.imwrite(img_name, frame) # capture and save image
						# send email with image
						sender.sendmail(sendTo, emailSubject, emailContent, img_name)
						# upload image and time stamp to Firebase
						fireCloud.upload(img_name)
						# check time here
						stop = time.time()
						print("Time to act upon intrusion= ", round(stop - start, 2), "seconds")
					
						time.sleep(2)
						# kill the program
						# update the FPS counter
						fps.update()
						fps.stop()
						cv2.destroyAllWindows()
						vs.stop()
						exit()
					
					
			
		else : 
			#GPIO.output(LED_PIN, GPIO.LOW) 
			lcd.text("",1)
			lcd.text("",2)
			lcd.text("",3)
			#check if door is closed then kill the program
			if GPIO.input(DOOR) == 0 :
				break # finish until the door is opened again

