import time
import board
import busio
import digitalio

from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

import subprocess


# Define the Reset Pin
oled_reset = digitalio.DigitalInOut(board.D4)

# Display Parameters
WIDTH = 128
HEIGHT = 64
BORDER = 5

# Display Refresh
LOOPTIME = 1.0

# Use for I2C.
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C, reset=oled_reset)

# Clear display.
oled.fill(0)
oled.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = oled.width
height = oled.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Load default font.
font = ImageFont.load_default()

# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype('PixelOperator.ttf', 16)
icon_font_small = ImageFont.truetype('fontawesome-webfont.ttf', 14)
icon_font_large = ImageFont.truetype('fontawesome-webfont.ttf', 16)

while True:

    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "hostname -I | cut -d\' \' -f1 | head --bytes -1"
    IP = subprocess.check_output(cmd, shell = True )

    cmd = "top -bn1 | grep load | awk '{printf \"CPU %.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell = True )

    cmd = "free -m | awk 'NR==2{printf \"%.2f%%\", $3*100/$2 }'"    
    MemUsage = subprocess.check_output(cmd, shell = True )
    
    cmd = "df -h | awk '$NF==\"/\"{printf \"HDD: %d/%dGB %s\", $3,$2,$5}'"
    cmd = "df -h | awk '$NF==\"/\"{printf \"%s\", $5}'"
    Disk = subprocess.check_output(cmd, shell = True )
    
    cmd = "vcgencmd measure_temp | cut -d '=' -f 2 | head --bytes -1"
    Temperature = subprocess.check_output(cmd, shell = True )

    # Icons
    # Icon temperature
    draw.text((x, top+5),    chr(62152),  font=icon_font_large, fill=255)
    # Icon memory
    draw.text((x+60, top+5), chr(62171),  font=icon_font_large, fill=255)
    # Icon disk
    draw.text((x, top+30), chr(61888),  font=icon_font_small, fill=255)
    # Icon Wifi
    draw.text((x, top+52), chr(61931),  font=icon_font_small, fill=255)

  # Text temperature
    draw.text((x+15, top+5), str(Temperature,'utf-8'),  font=font, fill=255)
  # Text mem usage
    draw.text((x+80, top+5), str(MemUsage,'utf-8'),  font=font, fill=255)
  # Text Disk usage
    draw.text((x+15, top+30), str(Disk,'utf-8'),  font=font, fill=255)
  # Text cpu usage
    draw.text((x+60, top+30), str(CPU,'utf-8'), font=font, fill=255)
  # Text IP address
    draw.text((x+15, top+49), str(IP,'utf-8'),  font=font, fill=255)
    
   # Display image.
    oled.image(image)
    oled.show()
    time.sleep(LOOPTIME)
