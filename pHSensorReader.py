#import relevant libraries
import spidev
import RPi.GPIO as GPIO
import time
import sys

# set up GPIO pin configuration
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(21, GPIO.OUT)

servo = GPIO.PWM(21, 50)
servo.start(2.5)

# set up SPI 
spi = spidev.SpiDev() #create spi object
spi.open(0, 0) #open spi port 0, device (CS) 0, for the MCP3008
spi.max_speed_hz=1000000

#configure analog to digital chip pin configuration
def readadc(adcnum): #read out the ADC
    if ((adcnum > 7) or (adcnum < 0)):
        return -1
    r = spi.xfer2([1, (8 + adcnum) << 4, 0])
    adcout = ((r[1] & 3) << 8) + r[2]
    return adcout

while True:
    returnedValue = readadc(1) #read adc channel 1
    calculatedValue = float(returnedValue / 1024) * (3.3 / 1000) #reading is in millivolts
    pHValue = (14 - (4665 * calculatedValue * 1.045))
    print ("pH Value = ", round(pHValue, 5))
    time.sleep(10)
