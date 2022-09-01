#!/usr/bin/env python3
# Created by: Michael Klements & Wesley de Vree (Macley(kun))
# For Raspberry Pi Desktop Case with OLED Stats Display
# Base on Adafruit CircuitPython & SSD1306 Libraries
# Installation & Setup Instructions - https://www.the-diy-life.com/add-an-oled-stats-display-to-raspberry-pi-os-bullseye/
import time
import board
import busio
import digitalio
import adafruit_ssd1306
import subprocess
import datetime
from PIL import Image, ImageDraw, ImageFont

def time_in_range(start, end, current):
    # Returns whether current is in the range [start, end]
    return start <= current <= end

# Display Parameters
width = 128
height = 64

# Font size
font_sz = 16

# When the display should be on e.g. 8:30 (8, 30, 0) up to 23:00
start = datetime.time(0, 0, 0)
end = datetime.time(0, 0, 0)
current = datetime.datetime.now().time()

# Methode to control the display with oled func
oled = adafruit_ssd1306.SSD1306_I2C(width, height, board.I2C(), addr=0x3C, reset=digitalio.DigitalInOut(board.D4))

# Clear display.
oled.fill(0)
oled.show()

# Create a blank image for drawing in 1-bit color
image = Image.new('1', (oled.width, oled.height))

# Get drawing object to draw on image
draw = ImageDraw.Draw(image)

# Import custom fonts
font = ImageFont.truetype('PixelOperator.ttf', font_sz)
icon_font= ImageFont.truetype('lineawesome-webfont.ttf', font_sz)
while True:
    while (time_in_range(start, end, current)):
        current = datetime.datetime.now().time()
        draw.rectangle((0, 0, oled.width, oled.height), fill=0) # Draw a black filled box to clear the image.
        cmd = "ip addr | awk '/inet / { print $2 }' | sed -n '2{p;q}' | cut -d '/' -f1" # Command that's executed in bash
        IP = subprocess.check_output(cmd, shell = True ) # Register ouput from cmd in var
        cmd = "vmstat 4 2|tail -1|awk '{print 100-$15}' | tr -d '\n'" # Takes a second to fetch for accurate cpu usage in %
        CPU = subprocess.check_output(cmd, shell = True )
        cmd = "free -m | awk 'NR==2{printf $3}'| awk '{printf $1/1000}'"
        Memuse = subprocess.check_output(cmd, shell = True )
        cmd = "cat /proc/meminfo | head -n 1 | awk -v CONVFMT='%.0f' '{printf $2/1000000}'"
        MemTotal = subprocess.check_output(cmd, shell = True )
        cmd = "free -m | awk -v CONVFMT='%.1f' 'NR==2{printf $3*100/$2}'"
        Memuseper = subprocess.check_output(cmd, shell = True )
        cmd = "df -h | awk '$NF==\"/\"{printf \"%s\", $5}'"
        Disk = subprocess.check_output(cmd, shell = True )
        cmd = "uptime | awk '{print $3,$4}' | cut -f1 -d','"
        uptime = subprocess.check_output(cmd, shell = True )
        cmd = "cat /sys/class/thermal/thermal_zone*/temp | awk -v CONVFMT='%.1f' '{printf $1/1000}'"   
        temp = subprocess.check_output(cmd, shell = True )
    
        # We draw the icons seprately and offset by a fixed amount later
        # Icon wifi, chr num comes from unicode &#xf1eb; to decimal 61931 (Use: https://www.binaryhexconverter.com/hex-to-decimal-converter)
        draw.text((1, 0), chr(61931), font=icon_font, fill=255) # Offset the icon on the x-as a little and devide the y-as in steps of 16
        # Icon cpu
        draw.text((1, 16), chr(62171), font=icon_font, fill=255)
        # Icon temp right
        draw.text((111, 16), chr(62153), font=icon_font, fill=255) # Offset the icon from the left to the farthest right
        # Icon memory
        draw.text((1, 32), chr(62776), font=icon_font, fill=255)
        # Icon disk
        draw.text((1, 48), chr(63426), font=icon_font, fill=255)
        # Icon time right
        draw.text((111, 48), chr(62034), font=icon_font, fill=255)
    
        # Pi Stats Display, printed from left to right each line
        draw.text((22, 0), str(IP,'utf-8'), font=font, fill=255) # x y followed by the content to be printed on the display followed by how it should be printed
        draw.text((22, 16), str(CPU,'utf-8') + "%", font=font, fill=255)
        draw.text((107, 16), str(temp,'utf-8') + "°C", font=font, fill=255, anchor="ra") # anchor basically refers to printing right to left: https://pillow.readthedocs.io/en/stable/handbook/text-anchors.html#specifying-an-anchor
        draw.text((22, 32), str(Memuseper,'utf-8') + "%", font=font, fill=255)
        draw.text((125, 32), str(Memuse,'utf-8') + "/" + str(MemTotal,'utf-8') + "G", font=font, fill=255, anchor="ra")
        draw.text((22, 48), str(Disk,'utf-8'), font=font, fill=255)
        draw.text((107, 48), str(uptime,'utf-8'), font=font, fill=255, anchor="ra")
    
        # Display image
        oled.image(image)
        oled.show()
        time.sleep(0)
    else:
        oled.fill(0)
        oled.show()
        sleep(60)
        current = datetime.datetime.now().time()
