#	Tested with python2.7 on raspberry PI 3 the 21/05/2018
#	Tested with Python2.7 on Ubuntu the 19 mai 2018
#	When the button is pressed it takes a picture and then speak itusing google speech engine
#
#	$sudo pip2 install pytesseract
#	$sudo apt-get install tesseract-ocr
#	$pip instal SpeechRecognition
#	$sudo pip install gTTS
#	install pa_stable_v190600_20161030.tgz : ./configure && sudo make install
#	install PyAudio-0.2.11.tar.gz : sudo python setup.py install
#
#	$jackd -r -d alsa 44100

import cv2
import numpy as np
import pytesseract
import picamera
from gtts import gTTS
import os
import time
from PIL import Image
import RPi.GPIO as GPIO
from gtts import gTTS

###############################################################################
##
###############################################################################
def say_something(msg):
	
	print("=>say_something() : " + msg)

	tts = gTTS(text=msg , lang='fr')
	tts.save("result.mp3")
	os.system("mpg123 result.mp3")


############################################################################
def get_string(img_path):

    # Read image with opencv
  with picamera.PiCamera() as camera:
    camera.resolution = (1024, 720)
    camera.capture("f1.jpg")   
    print("picture taken.")
#    capture = cv2.imread(img_path) 
#    time.sleep(1)

    # Recognize text with tesseract for python
    result = pytesseract.image_to_string(Image.open(img_path))
    return result
  

############################################################################
def read_picture():
	print ('--- Start recognize text from image ---')

	result1=get_string("f1.jpg")

	print (result1)
	time.sleep(1)

	try:
		tts = gTTS(text=result1 , lang='fr')
		#tts = gTTS(text="ceci est un test" , lang='fr')
		tts.save("result.mp3")
		os.system("mpg123 result.mp3")

	except AssertionError as e:
		print('Exception' + str(e)) 

	print ("------ Done -------")

############################################################################
if __name__ == "__main__":

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    while 1:
        bouton = GPIO.input(3)
        if bouton==0 :
            print("Button was pushed")
            read_picture()
            time.sleep(2)
        else:
            time.sleep(1)
    
