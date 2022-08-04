#psutil version coded by Jurgen Pfeifer
#Extends compatability, should run on Debian and Ubuntu
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
import time
import psutil as PS
import socket
import board
import digitalio
import adafruit_ssd1306
#
from PIL import Image, ImageDraw, ImageFont
#
KB=1024
MB=KB*1024
GB=MB*1024
#
WIDTH = 128
HEIGHT = 64
FONTSIZE = 16
#
LOOPTIME = 1.0
#
# Examples for usage:
#    IP = get_ipv4_from_interface("eth0")
#    IP = get_ipv4_from_interface("wlan0")
def get_ipv4_from_interface(interfacename):
    res="IP ?"
    try:
        iface=PS.net_if_addrs()[interfacename]
        for addr in iface:
            if addr.family is socket.AddressFamily.AF_INET:
                return "IP {0}".format(addr.address)
    except:
        return res
    return res

# This looks for the first IPv4 address that is not on the
# loopback interface. There is no guarantee on the order of
# the interfaces in the enumeration. If you've multiple interfaces
# and want to ensure to get an IPv4 address from a dedicated adapter,
# use the previous method.
def get_ipv4():
    ifaces=PS.net_if_addrs()
    for key in ifaces:
        if (key!="lo"): # Ignore the loopback interface
            # if it's not loopback, we look for the first IPv4 address    
            iface = ifaces[key]
            for addr in iface:
                if addr.family is socket.AddressFamily.AF_INET:
                    return "IP {0}".format(addr.address)
    return "IP ?"
#
# Use for I2C.
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C)

# Clear display.
oled.fill(0)
oled.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new("1", (oled.width, oled.height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box
draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)

padding = -2
top = padding
bottom = oled.height-padding
x = 0

# font = ImageFont.load_default()
font = ImageFont.truetype('PixelOperator.ttf', FONTSIZE)

while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,oled.width,oled.height), outline=0, fill=0)

    IP = get_ipv4()
    # IP = get_ipv4_from_interface("eth0") # Alternative
    
    CPU = "CPU {:.1f}%".format(round(PS.cpu_percent(),1))

    temps=PS.sensors_temperatures()
    TEMP= "{:.1f}°C".format(round(temps['cpu_thermal'][0].current,1))

    mem=PS.virtual_memory()
    MemUsage = "Mem {:5d}/{:5d}MB".format(round((mem.used+MB-1)/MB),round((mem.total+MB-1)/MB))

    root=PS.disk_usage("/")
    Disk="Disk {:4d}/{:4d}GB".format(round((root.used+GB-1)/GB),round((root.total+GB-1)/GB))

    draw.text((x, top),             IP,       font=font, fill=255)
    draw.text((x, top+FONTSIZE),    CPU,      font=font, fill=255)
    draw.text((x+80,top+FONTSIZE),  TEMP,     font=font, fill=255)
    draw.text((x, top+2*FONTSIZE),  MemUsage, font=font, fill=255)
    draw.text((x, top+3*FONTSIZE),  Disk,     font=font, fill=255)

    # Display image
    oled.image(image)
    oled.show()
    time.sleep(LOOPTIME)
