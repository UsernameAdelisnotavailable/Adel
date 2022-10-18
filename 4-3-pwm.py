import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.OUT)
frequency = 100
p = GPIO.PWM(22, frequency)
p.start(0)

try:
    while True:
        a = int(input("Enter new Duty Cycle value: "))
        p.ChangeDutyCycle(a)
except KeyboardInterrupt:
    print('\nThe program was stopped by the keyboard')
else:
    print('No exceptions')
finally:
    GPIO.cleanup()
