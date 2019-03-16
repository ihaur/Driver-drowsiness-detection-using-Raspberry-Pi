#!/usr/bin/env python3                                                                                

import speech_recognition as sr
from gtts import gTTS
import os

def get_vocal_command():
        
        r = sr.Recognizer()                                                                                   
        with sr.Microphone() as source:
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

def say_something(msg):
        
        print("=>say_something() : " + msg)

        tts = gTTS(text=msg , lang='fr')
        tts.save("result.mp3")
        os.system("mpg123 result.mp3")


        
t =None
while(t == None):
    t = get_vocal_command()
    print(t)
