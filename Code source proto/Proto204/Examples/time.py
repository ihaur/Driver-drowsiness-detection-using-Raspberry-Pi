# -*- coding: utf8 -*-
# coding : utf8

import time
import datetime

###############################################################################
###############################################################################
def print_date():

	# Get local date and time
	date = datetime.datetime.now()

	# Speak the date and time    
        msg_to_say = "Nous sommes le " + str(date.day) + " " + str(date.month) + " " + " deux mille dix huit " #str(date.year)
        msg_to_say += " Il est " + str(date.hour) + " heure et " + str(date.minute) + " minutes"
        print(msg_to_say)


############################################################################
if __name__ == "__main__":

	print_date()
