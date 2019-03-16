# -*- coding: utf8 -*-
# coding : utf8

import pyowm

###############################################################################
#	It is possible to give more informations from retrieved object.
#	Cf. https://github.com/csparpa/pyowm/blob/master/pyowm/docs/usage-examples.md
###############################################################################
def print_weather():

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
	msg_to_say = u"A Paris, il fait " + str(t['temp']) + u" degrés et le niveau d'humidité est  " + str(h)
 	msg_to_say += u" pour cent. La vitesse du vent est " + str(wi['speed']) + u" kilomètre heure "
        print(msg_to_say)
 

############################################################################
if __name__ == "__main__":
	
	print_weather()

