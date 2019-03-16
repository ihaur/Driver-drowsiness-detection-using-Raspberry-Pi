# -*- coding: utf8 -*-
# coding : utf8

#	Tested with python2.7 on raspberry PI 3 the 21/05/2018
#	Tested with Python2.7 on Ubuntu the 19 mai 2018
#	When the button is pressed it takes a picture and then speak itusing google speech engine
#
#	$sudo pip install pyowm
#	$sudo pip2 install pytesseract
#	$sudo apt-get install tesseract-ocr
#	$sudo pip --no-cache-dir install SpeechRecognition
#	$sudo pip install gTTS
#	install pa_stable_v190600_20161030.tgz : ./configure && sudo make install
#	install PyAudio-0.2.11.tar.gz : sudo python setup.py install
#	$sudo apt install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0 ffmpeg libav-tools	???
#
#	https://openclassrooms.com/forum/sujet/installation-pyaudio?page=1
#	With pa_stable_v190600_20161030.tgz
#
#	React to : 'hello' 'date' 'time' 'weather' 'email' 'events
#
#	$sudo apt-get install flac
#
#	$jackd -r -d alsa 44100

from __future__ import print_function
from googleapiclient import discovery
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from gtts import gTTS
import time
import datetime
import pyowm
import os
import sys
import speech_recognition as sr
import pyowm
import RPi.GPIO as GPIO



###############################################################################
##	React to vocal commands : 'date', "météo", "médicaments", "mail", "événements"
###############################################################################
def main_loop():

	global r
	global source

	r = sr.Recognizer()

        with sr.Microphone(device_index=1) as source:
  		r.adjust_for_ambient_noise(source, duration = 1)
                r.energy_threshold =1000
                print("Say something !")
                              
                audio = r.listen(source,None,2)
                print("Trying to recognize audio")

                try:
                        t=r.recognize_google(audio, language='fr_FR')
                        print ("You just said : " +t)
                        
                        if(t.find("date")!=-1):
                            print("=>date")
                            speak_date()
                                
                        elif(t.encode("utf-8").find("météo")!=-1):
                            print(u"=>météo")
                            speak_weather()
                        
                        elif(t.encode("utf-8").find("médicament")!=-1):
                            print(u"=>médicaments")
                            say_something(u"N oubliez pas de prendre votre doliprane à 18 heure")
                            
                        elif(t.find("mail")!=-1):
                            	print(u"=>mail")
				speak_email()

                        elif(t.encode("utf-8").find("événement")!=-1):	# évênement !!! Souci !
                            	print(u"=>évènements")
				speak_calendar()
                                
                except sr.UnknownValueError:
                        print("Google Speech Recognition could not understand audio")
                        say_something(u"Merci de répété votre demande")    

                except sr.RequestError as e:
                        print("Could not request results from Google Speech Recognition service; {0}".format(e))


###############################################################################
###############################################################################
def get_vocal_command():

	global r
	global source

	print("Say something !")
	audio = r.listen(source,None,2)

        try:
                t=r.recognize_google(audio, language='fr_FR')
                print ("You just said : " +t)
		return t
                      
        except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
                say_something(u"Merci de répété votre demande")    

        except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))


###############################################################################
###############################################################################
def say_something(msg):
	
	print("=>say_something() : " + msg)

	tts = gTTS(text=msg , lang='fr')
	tts.save("result.mp3")
	os.system("mpg123 result.mp3")


###############################################################################
###############################################################################
def speak_date():

	# Get local date and time
	date = datetime.datetime.now()

	# Speak the date and time    
        msg_to_say = "Nous sommes le " + str(date.day) + " " + str(date.month) + " " + " deux mille dix huit " #str(date.year)
        msg_to_say += " Il est " + str(date.hour) + " heure et " + str(date.minute) + " minutes"
        say_something(msg_to_say)


###############################################################################
#	It is possible to give more informations from retrieved object.
#	Cf. https://github.com/csparpa/pyowm/blob/master/pyowm/docs/usage-examples.md
###############################################################################
def speak_weather():

	# Initialize API access
	owm = pyowm.OWM('38e32c9eea23385bc6fa2e452f821eb5') 

	# Get current weather in Paris
	observation = owm.weather_at_place('Paris,FR')
	w = observation.get_weather()

	# Weather details
	wi=w.get_wind()
	h=w.get_humidity()
	t=w.get_temperature('celsius')

	# Speak the weather report
	msg_to_say = u"Il fait " + str(t['temp']) + u" degrés et le niveau d'humidité est  " + str(h)
 	msg_to_say += u" pour cent. La vitesse du vent est " + str(wi['speed']) + u" kilomètre heure "
        say_something(msg_to_say)


###############################################################################
def speak_calendar():

	# Setup the Calendar API
	SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
	store = file.Storage('credentials_cal.json')
	creds = store.get()
	if not creds or creds.invalid:
	    flow = client.flow_from_clientsecrets('client_id.json', SCOPES)
	    creds = tools.run_flow(flow, store)
	service = build('calendar', 'v3', http=creds.authorize(Http()))

	# Call the Calendar API to get 5 events
	now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
	events_result = service.events().list(calendarId='primary', timeMin=now, maxResults=5, singleEvents=True, orderBy='startTime').execute()
	events = events_result.get('items', [])

	# Reading the events
	for event in events:

		start_date = event['start'].get('dateTime', event['start'].get('date'))
		print(start_date, event['summary'])

		try :
			start_date_troncated = start_date[0:-6]
			eventdate = time.strptime(start_date_troncated, '%Y-%m-%dT%H:%M:%S')

		except Exception as e:
			#print("No hour")
			eventdate = time.strptime(start_date, '%Y-%m-%d')

		msg_to_say = u" " + str(event['summary']) + " le " + str(eventdate.tm_mday) + " " + str(eventdate.tm_mon) + " deux mille dix huit "	# + str(eventdate.tm_year)
		say_something(msg_to_say)

	# Adding the taxi feature
	msg_to_say = u"Voulez vous commander un taxi ?"
	say_something(msg_to_say)

	vocal_command = get_vocal_command()

	if(vocal_command == None):
		return

	if(vocal_command.find("oui")!=-1):
            	print(u"=>Commander un taxi")
		msg_to_say = u"Très bien. Une demande de taxi a été faite."
		say_something(msg_to_say)

	elif(vocal_command.find("non")!=-1):
            	print(u"=>Ne pas commander de taxi")
		msg_to_say = u"D'accord."
		say_something(msg_to_say)


###############################################################################
def GetMessage(service, user_id, msg_id):
	"""Get a Message with given ID.

	Args:
	service: Authorized Gmail API service instance.
	user_id: User's email address. The special value "me"
	can be used to indicate the authenticated user.
	msg_id: The ID of the Message required.

	Returns:
	A Message.
	"""
	try:
		message = service.users().messages().get(userId=user_id, id=msg_id).execute()
		return message

	except Exception as e:
		print('Exception' + str(e))


###############################################################################
def ListMessagesWithLabels(service, user_id, label_ids=[]):
	"""List all Messages of the user's mailbox with label_ids applied.

	Args:
	service: Authorized Gmail API service instance.
	user_id: User's email address. The special value "me"
	can be used to indicate the authenticated user.
	label_ids: Only return Messages with these labelIds applied.

	Returns:
	List of Messages that have all required Labels applied. Note that the
	returned list contains Message IDs, you must use get with the
	appropriate id to get the details of a Message.
	"""
	try:
		response = service.users().messages().list(userId=user_id, labelIds=label_ids).execute()
		messages = []

		if 'messages' in response:
			messages.extend(response['messages'])

		msg_cmpt = 0

		for msg_id in response['messages']:
			msg_cmpt += 1
			current_msg = GetMessage(service, user_id, msg_id['id'])
			print ('Message %d : %s\n' % (msg_cmpt, current_msg['snippet']))

			# Read the message
			msg_to_say = u" " + current_msg['snippet']
			say_something(msg_to_say)

			msg_to_say = u"Voulez vous lire le message suivant ?"
			say_something(msg_to_say)

			vocal_command = get_vocal_command()
			if(vocal_command == None):
				return

			if(vocal_command.find("non")!=-1):
				msg_to_say = u"D'accord."
				say_something(msg_to_say)
				return


	except Exception as e:
		print('Exception' + str(e)) 


###############################################################################
def ListMessagesLabels(service, user_id, label_ids=[]):

	labels = results.get('labels', [])
	if not labels:
		print('No labels found.')
	else:
	    print('Labels:')
	    for label in labels:
	        print(label['name'])


###############################################################################
def speak_email():

	# Setup the Gmail API
	SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
	store = file.Storage('credentials_email.json')
	creds = store.get()

	if not creds or creds.invalid:
	    flow = client.flow_from_clientsecrets('client_id.json', SCOPES)
	    creds = tools.run_flow(flow, store)

	# Call the Gmail API
	service = build('gmail', 'v1', http=creds.authorize(Http()))
	ListMessagesWithLabels(service, 'me', 'UNREAD')
	#results = service.users().labels().list(userId='me').execute()


############################################################################
def list_microphones():
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print("Microphone with name \"{1}\" found for 'Microphone(device_index={0})'".format(index, name))
        
    print("\n\n")
    

############################################################################
if __name__ == "__main__":

	say_something("ceci est un test")

	# initialize Button 
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(32, GPIO.IN, pull_up_down=GPIO.PUD_UP)		# Right


	# main loop
	while 1:
		bouton = GPIO.input(32)
		if bouton==0 :
			main_loop()

