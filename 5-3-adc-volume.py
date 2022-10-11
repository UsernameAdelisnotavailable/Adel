import RPi.GPIO as GPIO
import time
dac = [26, 19, 13, 6, 5, 11, 9, 10]
leds = [21, 20, 16, 12, 7, 8, 25, 24]
comp = 4
troyka = 17
bits = len(dac)
maxVoltage = 3.3
levels = 2**bits
GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comp, GPIO.OUT)
GPIO.setup(leds, GPIO.OUT)
def decimal2binary(value):
    return [int(element) for element in bin(value)[2:].zfill(8)]
def adc(value):
    signal = decimal2binary(value)
    GPIO.output(dac, signal)
    return signal
def binary2decimal(signal):
    value = 0
    for i in range(len(signal)):
        value += signal[i] * (2 ** (7 -i))
    return value
try:
    a = 1
    while a == 1:
        signal = [0, 0, 0, 0, 0, 0, 0, 0]
        for bit in range(bits):
            signal[bit] = 1
            value = binary2decimal(signal)
            signal = adc(value)
            time.sleep(0.001)
            compValue = GPIO.input(comp)
            if compValue == 0:
                signal[bit] = 0
                value = binary2decimal(signal)

        voltage = value/levels * maxVoltage
        print(value, signal, voltage)
        volume = [0, 0, 0, 0, 0, 0, 0, 0]
        for bit in range(bits):
            if value > 0:
                volume[bit] = 1
            value = value - 7
        GPIO.output(leds, volume)


except KeyboardInterrupt:
    print('\nThe program was stopped by the keyboard')
else:
    print('No exceptions')
finally:
    GPIO.output(dac,GPIO.LOW)
    GPIO.cleanup()