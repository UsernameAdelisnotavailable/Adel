import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(15, GPIO.IN)
GPIO.setup(14, GPIO.OUT)
GPIO.output(14, GPIO.input(15))