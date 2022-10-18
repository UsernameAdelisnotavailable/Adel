import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
import time

leds = [21, 20, 16, 12, 7, 8, 25, 24]                                  #список переменных
dac = [26, 19, 13, 6, 5, 11, 9, 10]
comp = 4
troyka = 17
bits = len(dac)
maxVoltage = 3.3
levels = 2**bits
counter = 0

GPIO.setmode(GPIO.BCM)                                                 #настройка GPIO
GPIO.setup(leds, GPIO.OUT)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(comp, GPIO.IN)
GPIO.setup(troyka, GPIO.OUT)

def decimal2binary(value):                                             #функция перевода числа в сигнал
    return [int(element) for element in bin(value)[2:].zfill(8)]

def adc(value):                                                        #функция вывода значения на DAC
    signal = decimal2binary(value)
    GPIO.output(dac, signal)
    return signal

def binary2decimal(signal):                                            #функция перевода сигнала в число
    value = 0
    for i in range(len(signal)):
        value += signal[i] * (2 ** (7 -i))
    return value

def get_voltage():                                                     #функция измерения напряжения на тройке
    signal = [0, 0, 0, 0, 0, 0, 0, 0]
    for bit in range(bits):
        signal[bit] = 1
        value = binary2decimal(signal)
        signal = adc(value)
        time.sleep(0.005)
        compValue = GPIO.input(comp)
        if compValue == 0:
            signal[bit] = 0
            value = binary2decimal(signal)
    return value

def show_voltage(value):                                                #функция вывода сигнала на светодиоды
    signal = decimal2binary(value)
    GPIO.output(leds, signal)

try:                                                                    #исполняемая часть кода
    measured_data = []                                                  #пустой список для добавления измерений
    starting_momemt = time.time()                                       #начальный момент времени
    
    voltage = 0
    GPIO.output(troyka, 1)                                              #подача напряжения 3.3В на тройку
    print("Capacitor charging")
    while (voltage <= 0.97 * maxVoltage):
        value = get_voltage()                                           #измерение напряжения на тройке
        show_voltage(value)
        voltage = value/levels * maxVoltage
        measured_data.append(value)                                   #добавление измерений в список
        counter += 1

    GPIO.output(troyka, 0)                                              #подача напряжения 0.0В на тройку
    print("Discharging")
    while (voltage >= 0.02 * maxVoltage):
        value = get_voltage()                                           #измерение напряжения на тройке
        show_voltage(value)
        voltage = value/levels * maxVoltage
        measured_data.append(value)                                   #добавление измерений в список
        counter += 1
    
    finish_moment = time.time()                                         #время завершения измерений
    
    exp_running_time = finish_moment - starting_momemt
                                                                        #подолжительность эксперимента
    plt.plot(measured_data)
    plt.show()                                                          #построение графика
    
    measured_data_str = [str(item) for item in measured_data]
    with open("data.txt", "w") as outfile:                              #показания АЦП
        outfile.write("\n".join(measured_data_str))


    with open("settings.txt", "w") as outfile:                          #средняя частота дискретизации и шаг квантования
        outfile.write("Частота дискретизации 200Гц, шаг квантования 0,01289В")

    print("Experiment running time", exp_running_time, "seconds")       #вывод в терминал продолжительности и периода эксперимета, частоты дискретизации и шага квантования
    print("Exp. period ", exp_running_time / counter, "seconds")
    print("Sampl frequency", counter / exp_running_time, "Hz")
    print("Quantization step 3.3/256 ~ 0.01289 V")

except KeyboardInterrupt:
    print('\nThe program was stopped by the keyboard')

finally:
    GPIO.output(dac,GPIO.LOW)
    GPIO.output(leds,GPIO.LOW)
    GPIO.cleanup()