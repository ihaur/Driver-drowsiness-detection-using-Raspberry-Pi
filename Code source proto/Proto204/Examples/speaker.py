# -*- coding: utf8 -*-
# coding : utf8

from gtts import gTTS
import os

###############################################################################
###############################################################################
def say_something(msg):
	
	print("=>" + msg)

	tts = gTTS(text=msg , lang='fr')
	tts.save("result.mp3")
	os.system("mpg123 result.mp3")


############################################################################
if __name__ == "__main__":

	say_something("Test du haut parleur")

