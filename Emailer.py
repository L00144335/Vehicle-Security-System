# import necessary libraries and packages
import smtplib # SMTP services
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

#class to be used for the email
class Emailer :
	
	def sendmail(self, recipient, subject, content, image):
		
		SMTP_SERVER = "smtp.gmail.com"
		SMTP_PORT = 587
		GMAIL_USERNAME = "yourcaralert@gmail.com" #yourCarAlert
		GMAIL_PASSWORD = "raspberryPi77"
		
		#Create Headers
		emailData = MIMEMultipart()
		emailData['Subject'] = subject
		emailData['To'] = recipient
		emailData['From'] = GMAIL_USERNAME
		
		# Attach data here
		emailData.attach(MIMEText(content))
		
		#Create our Image Data from the defined image
		imageData = MIMEImage(open(image, 'rb').read(), 'jpg')
		imageData.add_header('Content-Disposition', 'attachment; filename="intruder.jpg"')
		emailData.attach(imageData)

		#Connect to Gmail Server
		session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
		session.ehlo()
		session.starttls()
		session.ehlo()

		#Login to Gmail
		session.login(GMAIL_USERNAME, GMAIL_PASSWORD)

		#Send Email & Exit
		session.sendmail(GMAIL_USERNAME, recipient, emailData.as_string())
		session.quit

		
	
	# end of email class
