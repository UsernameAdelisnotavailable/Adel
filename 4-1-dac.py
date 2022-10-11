'''import RPi.GPIO as GPIO

dac = [26, 19, 13, 6, 5, 11, 9, 10]
GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)

def decimal2binary(value):
    return [int(element) for element in bin(value)[2:].zfill(8)]

a = 255
try:
    while (a < 256):
        a = int(input('Введите число от 0 до 255: '))
        GPIO.output(dac, decimal2binary(a))
        print(3.3 * a/256, 'Вольт')
finally:
    GPIO.cleanup()'''

import RPi.GPIO as GPIO
dac = [26, 19, 13, 6, 5, 11, 9, 10]
bits = len(dac)
levels = 2**bits
bits = len(dac)
maxVoltage = 3.3
comp = 4
troyka = 17
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
        inputStr = input()
        
        if inputStr.isdigit():
            value = int(inputStr)
        
            if value > 255:
                print('The value is too large')
                continue
            
            signal = adc(value)
            voltage = value/levels * maxVoltage
            print(voltage)

        elif inputStr == 'q':
            break;
        else:
            print('Enter a positive number')
            continue
        
except KeyboardInterrupt:
    print('\nThe program was stopped by the keyboard')
else:
    print('No exceptions')
finally:
    GPIO.output(dac,GPIO.LOW)
    GPIO.cleanup(dac)
