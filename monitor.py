# Created by: Michael Klements
# For Raspberry Pi Desktop Case with OLED Stats Display
# Base on Adafruit Blinka & SSD1306 Libraries
# Installation & Setup Instructions - https://www.the-diy-life.com/add-an-oled-stats-display-to-raspberry-pi-os-bullseye/
import time
import board
import busio
import gpiozero

from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

import subprocess

# Define the Reset Pin using gpiozero
oled_reset = gpiozero.OutputDevice(4, active_high=False)  # GPIO 4 (D4) used for reset

# Display Parameters
WIDTH = 128
HEIGHT = 64
BORDER = 5

# Display Refresh
LOOPTIME = 1.0

# Use I2C for communication
i2c = board.I2C()

# Manually reset the display (high -> low -> high for reset pulse)
oled_reset.on()  # Set the reset pin high
time.sleep(0.1)  # Delay for a brief moment
oled_reset.off()  # Toggle reset pin low
time.sleep(0.1)  # Wait for reset
oled_reset.on()  # Turn reset pin back high

# Create the OLED display object
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C)

# Clear the display
oled.fill(0)
oled.show()

# Create a blank image for drawing
width = oled.width
height = oled.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image
draw.rectangle((0, 0, width, height), outline=0, fill=0)

# Draw some shapes
padding = -2
top = padding
bottom = height - padding
x = 0

# Load default font
font = ImageFont.load_default()

# Alternatively load a TTF font. Make sure the .ttf font file is in the same directory as the python script!
font = ImageFont.truetype('PixelOperator.ttf', 16)
icon_font = ImageFont.truetype('lineawesome-webfont.ttf', 18)

while True:
    # Draw a black filled box to clear the image
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Shell scripts for system monitoring
    cmd = "hostname -I | cut -d\' \' -f1 | head --bytes -1"
    IP = subprocess.check_output(cmd, shell=True)

    cmd = "top -bn1 | grep load | awk '{printf \"%.2fLA\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell=True)

    cmd = "free -m | awk 'NR==2{printf \"%.2f%%\", $3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell=True)

    cmd = "df -h | awk '$NF==\"/\"{printf \"HDD: %d/%dGB %s\", $3,$2,$5}'"
    cmd = "df -h | awk '$NF==\"/\"{printf \"%d/%dGB\", $3,$2}'"
    Disk = subprocess.check_output(cmd, shell=True)

    cmd = "vcgencmd measure_temp | cut -d '=' -f 2 | head --bytes -1"
    Temperature = subprocess.check_output(cmd, shell=True)

    # Icons
    # Icon temperature
    draw.text((x, top + 5), chr(62609), font=icon_font, fill=255)
    # Icon memory
    draw.text((x + 65, top + 5), chr(62776), font=icon_font, fill=255)
    # Icon disk
    draw.text((x, top + 25), chr(63426), font=icon_font, fill=255)
    # Icon cpu
    draw.text((x + 65, top + 25), chr(62171), font=icon_font, fill=255)
    # Icon wifi
    draw.text((x, top + 45), chr(61931), font=icon_font, fill=255)

    # Text
    # Text temperature
    draw.text((x + 19, top + 5), str(Temperature, 'utf-8'), font=font, fill=255)
    # Text memory usage
    draw.text((x + 87, top + 5), str(MemUsage, 'utf-8'), font=font, fill=255)
    # Text Disk usage
    draw.text((x + 19, top + 25), str(Disk, 'utf-8'), font=font, fill=255)
    # Text cpu usage
    draw.text((x + 87, top + 25), str(CPU, 'utf-8'), font=font, fill=255)
    # Text IP address
    draw.text((x + 19, top + 45), str(IP, 'utf-8'), font=font, fill=255)

    # Display image
    oled.image(image)
    oled.show()
    
    # Wait for the next loop
    time.sleep(LOOPTIME)
