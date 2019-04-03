#!/usr/bin/env python3
import os
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from PIL import ImageFont
import smbus2
import bme280
import time
import os
def do_nothing(obj):
    pass


# define our i2c LED location
serial = i2c(port=1, address=0x3C)
# We have an ssd1306 device so we initialize it at the
# serial address we created.
device = ssd1306(serial)
# This line keeps the display from immediately turning off once the
# script is complete.
device.cleanup = do_nothing

# Setup our Temperature sensor (bme280)
port = 4
address = 0x76
bus = smbus2.SMBus(port)
calibration_params = bme280.load_calibration_params(bus, address)
font = ImageFont.truetype('/usr/share/fonts/truetype/FreeMono.ttf', 10) 
# the sample method will take a single reading and return a
# compensated_reading object
def temperature():    
    data = bme280.sample(bus, address, calibration_params)
    return "%0.0fF" % ((data.temperature*9/5 +32))
data = bme280.sample(bus, address, calibration_params)
def main():
    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white", fill="black")
        draw.text((45,20), temperature(),font = font ,fill="white")
        draw.text((35,5),"Temperature",font=font,fill="white")
        draw.text((45,45), ("%3.1f" %(data.humidity)),font = font, fill='white')
        draw.text((35,30), "Humidity",font=font,fill='white')
        draw.text((5, 55), date_time(), font=font, fill='white')
def lan_ip():
    cmd = 'hostname -I'
    f = popen(cmd)
    ip = str(f.read())
    return "IP: %s" % ip.rstrip('/r/n').rstrip(' ')
def date_time():
    f = os.popen('date +"%a %x %H:%M:%S"')
    dt = str(f.read())
    return "%s" % dt.rstrip('/r/n').rstrip(' ')

while True:
    main()
    time.sleep(1)
    
    
    


