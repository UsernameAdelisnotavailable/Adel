import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.OUT)
p = GPIO.PWM(24, 2)

try:
    while True:
        a = int(input("Введите число от 0 до 100: "))
        p.start(a)
        input()
        p.stop()
finally:
    GPIO.cleanup()