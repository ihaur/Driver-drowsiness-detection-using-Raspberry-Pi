import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(32, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(36, GPIO.IN, pull_up_down=GPIO.PUD_UP)


print("Top : \t\t" + str(GPIO.input(16)))
print("Left : \t\t" + str(GPIO.input(18)))
print("Bottom : \t" + str(GPIO.input(22)))
print("Right : \t" + str(GPIO.input(36)))
print("Validate : \t" + str(GPIO.input(32)))
