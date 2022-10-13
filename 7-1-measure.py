import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt 

GPIO.setmode(GPIO.BCM)

comp = 4
troyka = 17
dac = [26, 19, 13, 6, 5, 11, 9, 10]
leds = [21, 20, 16, 12, 7, 8, 25, 24]
st = []
ret = 0

for i in dac: GPIO.setup(i, GPIO.OUT)
for j in leds: GPIO.setup(j, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT)
GPIO.setup(comp, GPIO.IN)

def dec2bin(value):
    return [int(elem) for elem in bin(value)[2:].zfill(8)]

def adc():
    ret = 0
    value = 0
    for j in range(7, -1 , -1):
        value = ret + 2**j
        binlist = dec2bin(value)
        for i in range(len(dac)): GPIO.output(dac[i], binlist[i])
        time.sleep(0.001)
        if GPIO.input(comp) == 1: ret += 2**j
    return ret

try:
    start = time.time()
    GPIO.output(17, 1)
    val = 0
    while(val < 220):
        val = adc()
        voltage = 3.3 * val / 256
        print(val, "{:.3}".format(voltage))
        st += [voltage]
        ledslist = dec2bin(2**(round(8*val/256))-1)
        for k in range(len(leds)): GPIO.output(leds[k], ledslist[k])
        if val > 230: break
    print('Charge is finished')
    GPIO.output(17, 0)
    while(val > 20):
        val = adc()
        voltage = 3.3 * val / 256
        print(val, "{:.3}".format(voltage))
        st += [voltage]
        ledslist = dec2bin(2**(round(8*val/256))-1)
        for k in range(len(leds)): GPIO.output(leds[k], ledslist[k])
    end = time.time()
    duration = end - start
    
    f = open('data.txt', 'w')
    g = open('settings.txt', 'w')
    
    for i in st: 
        f.write(str(i))
        f.write('\n')
    
    T = duration/len(st); frequency = "{:.3}".format(1/T); step = "{:.3}".format(3.3/256)
    
    g.write("Sampling frequency is "); g.write(frequency); g.write(" Hz"); g.write('\n')
    g.write("Quantization step is "); g.write(step); g.write(" Hz")
    
    print("Duration of the experiment is", "{:.3}".format(duration), "sec")
    print("Duration of one measurement is", "{:.3}".format(T), "sec")
    print("Sampling frequency is", frequency, "Hz")
    print("Quantization step is", step, "V")
    
    #stime = [T*i for i in range(len(st))]
    plt.plot(st)
    plt.show()

finally:
    for i in dac: GPIO.output(i, 0)
    for i in leds: GPIO.output(i, 0)
    GPIO.output(troyka, 0)
    GPIO.cleanup() 
    f.close()
    g.close()