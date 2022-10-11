import RPi.GPIO as GPIO
import time

dac = [26, 19, 13, 6, 5, 11, 9, 10]
GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)

def dec2bin(value):
    return [int(element) for element in bin(value)[2:].zfill(8)]
try:
    while(True):
        T = int(input("Период: "))/512
        for i in range(256):
            GPIO.output(dac, dec2bin(i))
            time.sleep(T)
        for i in range(255, -1, -1):
            GPIO.output(dac, dec2bin(i))
            time.sleep(T)
finally:
    GPIO.cleanup()
