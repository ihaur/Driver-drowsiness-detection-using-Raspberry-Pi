# coding=utf-8

import os
import subprocess
import time
import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from subprocess import call


# Init buttons variables
#########################

button_up = 23
button_left = 24
button_down = 25
button_right = 16
button_validate = 12

button_pushed = 0

nb_progs = None
menu_state = None
prog_state = None
file_list = None
my_subprocess = None

disp = Adafruit_SSD1306.SSD1306_128_32(rst=None)


################################################################################
#	$awk '{ split(FILENAME, array, "/"); print array[5] ": " $1 }' $(find /sys/class/net/*/operstate ! -type d)
################################################################################
def get_WIFI_state():

	cmd = """awk '{ split(FILENAME, array, "/"); print array[5] ": " $1 }' $(find /sys/class/net/*/operstate ! -type d)"""
	cmd_result = subprocess.check_output(cmd, shell = True )

	if (0 < cmd_result.find("up")):
		return "On"
	else :
		return "Off"


################################################################################
#	$hciconfig	bluetooth state
################################################################################
def get_BT_state():

	cmd = "hciconfig"
	cmd_result = subprocess.check_output(cmd, shell = True )

	if (0 < cmd_result.find("UP")):
		return "On"
	else :
		return "Off"

################################################################################
#
################################################################################
def init_screen():

	disp.begin()
	disp.clear()
	disp.display()

################################################################################
#	print(u"\u2193")	fleche vers le bas
#	print(u"\u2191")	fleche vers le haut
#
################################################################################
def print_menu(line_1, line_2, line_3):

	font = ImageFont.load_default()
	image = Image.new('1', (disp.width, disp.height))
	draw = ImageDraw.Draw(image)

	# Draw a black filled box to clear the image.
	draw.rectangle((0,0,disp.width,disp.height), outline=0, fill=0)

	line_4 = "Wifi " + get_WIFI_state() + " | BT " + get_BT_state()

	draw.text((0, -2),       line_1,  font=font, fill=255)
	draw.text((0, -2+8),     line_2, font=font, fill=255)
	draw.text((0, -2+16),    line_3,  font=font, fill=255)
	draw.text((0, -2+25),    line_4,  font=font, fill=255)

	# Display image.
	disp.image(image)
	disp.display()
	time.sleep(.1)


################################################################################
#
################################################################################
def button_pushed(channel):

	global button_pushed

	button_str = ""

	if (channel == button_up):
		button_str = "up"
	elif (channel == button_left):
		button_str = "left"
	elif (channel == button_down):
		button_str = "down"
	elif (channel == button_right):
		button_str = "right"
	elif (channel == button_validate):
		button_str = "validate"

#	print ("Button pushed : "  + button_str + " (" + str(channel) + ")")
	
	button_pushed = channel


################################################################################
#
################################################################################
def init_gpio():

	GPIO.setmode(GPIO.BCM)
	
	button_up = 23
	button_left = 24
	button_down = 25
	button_right = 16
	button_validate = 12
	
	GPIO.setup(button_up, GPIO.IN, pull_up_down=GPIO.PUD_UP)	# Top (Pin 16)
	GPIO.setup(button_left, GPIO.IN, pull_up_down=GPIO.PUD_UP)	# Left (Pin 18)
	GPIO.setup(button_down, GPIO.IN, pull_up_down=GPIO.PUD_UP)	# Bottom (Pin 22)
	GPIO.setup(button_validate, GPIO.IN, pull_up_down=GPIO.PUD_UP)	# Validate (Pin 32)
	GPIO.setup(button_right, GPIO.IN, pull_up_down=GPIO.PUD_UP)	# Right (Pin 36)

	GPIO.add_event_detect(button_up, GPIO.FALLING, callback=button_pushed)
	GPIO.add_event_detect(button_left, GPIO.FALLING, callback=button_pushed)
	GPIO.add_event_detect(button_down, GPIO.FALLING, callback=button_pushed)
	GPIO.add_event_detect(button_right, GPIO.FALLING, callback=button_pushed)
	GPIO.add_event_detect(button_validate, GPIO.FALLING, callback=button_pushed)


################################################################################
#	menu_state = -1	Welcome menu
#	menu_state = x	x program selected
#	prog_state = 0 : not running
#	prog_state = 1 : running
#	prog_state = 2 : ask if need to be stopped
################################################################################
def update_state():

	global menu_state
	global prog_state
	global button_pushed
	global nb_progs
	global file_list
	global my_subprocess

	print ("menu_state = " + str(menu_state) + " | prog_state = " + str(prog_state) + " | button = " + str(button_pushed))

	# Check process state
	try :
		process_state = my_subprocess.poll()
	except :
		pass
		#print("Process not initialized")


	# In main menu, prog not running
	if (0 == prog_state) and (button_pushed == button_up):
		menu_state = (menu_state - 1)%nb_progs
		
	elif (0 == prog_state) and (button_pushed == button_down):
		menu_state = (menu_state + 1)%nb_progs

	elif (0 == prog_state) and (button_pushed == button_right) and (-1 < menu_state):
		prog_state = prog_state + 1
		# Run program	
		my_subprocess = subprocess.Popen(["python", file_list[(menu_state+1)%nb_progs]])

	# Program running
	elif (1 == prog_state) and (process_state != None):
		print('Subprocess exited')
		prog_state = 0
		menu_state = -1
		
	elif (1 == prog_state) and (button_pushed == button_left):
		prog_state = 2

	# Asking if we need to stop the program
	elif (2 == prog_state) and (button_pushed == button_left):
		prog_state = 0
		menu_state = -1
		# Stopping prog
		my_subprocess.terminate()

	elif (2 == prog_state) and (button_pushed == button_right):
		prog_state = 1

	button_pushed = 0


################################################################################
#
################################################################################
if __name__ == '__main__':

	global nb_progs
	global menu_state
	global prog_state
	global file_list

	nb_progs = 0
	menu_state = -1
	prog_state = 0
	file_list = None
	my_subprocess = None	

	line_1 = None
	line_2 = None
	line_3 = None

	# Getting list of available programs	
	file_list = os.listdir('./')
	file_list = filter(lambda k: '.py' in k, file_list)
	file_list.remove("Proto204.py")
	nb_progs = len(file_list)

	init_gpio()
	init_screen()

	while True:

		if (-1 == menu_state):
			line_1 = "Hello IoT Dev."
			#line_2 = "Select prog. with " + u'\N{BLACK UP-POINTING TRIANGLE}'.encode("utf-8") #u'\u2193'.encode("utf-8")	
			line_2 = "Select prog. with"
			line_3 = "up and down arrows"
		else :
			if (0 == prog_state):
				line_1 = file_list[menu_state]
				line_2 = "=>" + file_list[(menu_state+1)%nb_progs]
				line_3 = file_list[(menu_state+2)%nb_progs]

			if (1 == prog_state):
				line_1 = file_list[(menu_state+1)%nb_progs]
				line_2 = "Running"
				line_3 = "press < to stop"

			if (2 == prog_state):
				line_1 = file_list[(menu_state+1)%nb_progs]
				line_2 = "Stop ? < Y / N >"
				line_3 = ""

		print_menu(line_1, line_2, line_3)
		update_state()
		time.sleep(0.5)
	
		# Check if the process finished



