# imports
import pyrebase

class Firebase :
	def upload(self, image):
		# declare credentials
		config = {
			"apiKey": "AIzaSyCwl7CFIamhtQeIq75gj-iyHifntE6r-Jc",
			"authDomain": "vehiclesecuritystorage.firebaseapp.com",
			"databaseURL": "https://vehiclesecuritystorage-default-rtdb.firebaseio.com",
			"projectId": "vehiclesecuritystorage",
			"storageBucket": "vehiclesecuritystorage.appspot.com",
			"serviceAccount": "serviceAccountKey.json" 
		}
		
		# init storage (provide config 
		firebase_storage = pyrebase.initialize_app(config)
		# connect to storage
		storage = firebase_storage.storage()
		
		# upload image
		storage.child(image).put(image)
		

		
