import RPi.GPIO as GPIO
import time
dac = [26, 19, 13, 6, 5, 11, 9, 10]
comp = 4
troyka = 17
bits = len(dac)
maxVoltage = 3.3
levels = 2**bits
GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comp, GPIO.OUT)
def decimal2binary(value):
    return [int(element) for element in bin(value)[2:].zfill(8)]
def adc(value):
    signal = decimal2binary(value)
    GPIO.output(dac, signal)
    return signal
try:
    while True:

        for value in range(256):            
            signal = adc(value)
            voltage = value/levels * maxVoltage
            time.sleep(0.001)
            compValue = GPIO.input(comp)
            if compValue == 0:
                print(value, signal, voltage)
                break

except KeyboardInterrupt:
    print('\nThe program was stopped by the keyboard')
else:
    print('No exceptions')
finally:
    GPIO.output(dac,GPIO.LOW)
    GPIO.cleanup()