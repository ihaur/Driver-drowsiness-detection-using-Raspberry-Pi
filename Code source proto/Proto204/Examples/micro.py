# -*- coding: utf8 -*-
# coding : utf8

#from __future__ import print_function
#from googleapiclient import discovery
#from googleapiclient.discovery import build
#from httplib2 import Http
#from oauth2client import file, client, tools
#from gtts import gTTS
#import pyowm
import speech_recognition as sr


###############################################################################
##	
###############################################################################
def get_vocal_command():

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
                                   
                except sr.UnknownValueError:
                        print("Google Speech Recognition could not understand audio")

                except sr.RequestError as e:
                        print("Could not request results from Google Speech Recognition service; {0}".format(e))


############################################################################
def list_microphones():
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print("Microphone with name \"{1}\" found for 'Microphone(device_index={0})'".format(index, name))
        
    print("\n\n")
    

############################################################################
if __name__ == "__main__":

	#list_microphones()
	get_vocal_command()


