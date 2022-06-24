#import relevant libraries
import time
import spidev
import RPi.GPIO as GPIO
import sys

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.virtual import viewport
from luma.core.render import canvas
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT

# set up GPIO pin configuration
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(21, GPIO.OUT)
servo = GPIO.PWM(21, 50)
servo.start(2.5)

# set up SPI for pH Sensor as main program focus
spiMain = spidev.SpiDev() #create spi object
spiMain.open(0, 0) #open spi port 0, device (CS) 0, for the MCP3008
spiMain.max_speed_hz=1000000

#configure analog to digital chip pin configuration
def readadc(adcnum): #read out the ADC
    if ((adcnum > 7) or (adcnum < 0)):
        return -1
    r = spiMain.xfer2([1, (8 + adcnum) << 4, 0])
    adcout = ((r[1] & 3) << 8) + r[2]
    return adcout

#configure device and call readadc function to retrieve input from pH sensor device
def main(n, block_orientation, rotate, inreverse):
    serial = spi(port=1, device=0, gpio=noop())
    device = max7219(serial, cascaded=n or 1, block_orientation = block_orientation, rotate=rotate or 0, blocks_arranged_in_reverse_order=inreverse)
    print("Created device")
    while True:
        returnedValue = readadc(1) #read adc channel 1
        calculatedValue = float(returnedValue / 1024) * (3.3 / 1000) #reading is in millivolts
        gainvalue = 4665
        calibrationValue = 1.045
        pHValue = (14 - (gainvalue * calculatedValue * calibrationValue))
        msg = str(round(pHValue, 2))
        print(msg)
        virtual = viewport(device, width=device.width, height=len(msg) * 8)
        with canvas(virtual) as draw:
            text(draw, (0, 0), msg, fill="red", font=proportional(CP437_FONT))
        time.sleep(10)

main(4, -90, 0, False)