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

# Use gpiozero to control the reset pin
oled_reset_pin = gpiozero.OutputDevice(4, active_high=False)  # GPIO 4 for reset, active low

# Display Parameters
WIDTH = 128
HEIGHT = 64
BORDER = 5

# Display Refresh
LOOPTIME = 1.0

# Use I2C for communication
i2c = board.I2C()

# Manually reset the display (high -> low -> high for reset pulse)
oled_reset_pin.on()
time.sleep(0.1)  # Delay for a brief moment
oled_reset_pin.off()  # Toggle reset pin low
time.sleep(0.1)  # Wait for reset
oled_reset_pin.on()  # Turn reset pin back high

# Create the OLED display object
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C)

# Clear the display
oled.fill(0)
oled.show()

# Create a blank image for drawing
image = Image.new("1", (oled.width, oled.height))

# Get drawing object to draw on image
draw = ImageDraw.Draw(image)

# Draw a white background
draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)

font = ImageFont.truetype('PixelOperator.ttf', 16)

while True:
    # Draw a black filled box to clear the image
    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)

    # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "hostname -I | cut -d\' \' -f1"
    IP = subprocess.check_output(cmd, shell=True)
    cmd = "top -bn1 | grep load | awk '{printf \"CPU: %.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell=True)
    cmd = "free -m | awk 'NR==2{printf \"%.1f %.1f %.1f\", $3/1024,$2/1024,($3/$2)*100}'"
    MemUsage = subprocess.check_output(cmd, shell=True)
    mem_parts = MemUsage.decode('utf-8').strip().split()
    mem_used_gb = mem_parts[0]
    mem_total_gb = mem_parts[1]
    mem_percent = mem_parts[2]
    mem_display = f"Mem: {mem_used_gb}/{mem_total_gb}GB {mem_percent}%"
    cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
    Disk = subprocess.check_output(cmd, shell=True)
    cmd = "vcgencmd measure_temp |cut -f 2 -d '='"
    Temp = subprocess.check_output(cmd, shell=True)

    # Pi Stats Display
    draw.text((0, 0), "IP: " + str(IP, 'utf-8'), font=font, fill=255)
    draw.text((0, 16), str(CPU, 'utf-8') + "LA", font=font, fill=255)
    draw.text((80, 16), str(Temp, 'utf-8'), font=font, fill=255)
    draw.text((0, 32), mem_display, font=font, fill=255)
    draw.text((0, 48), str(Disk, 'utf-8'), font=font, fill=255)

    # Display the image
    oled.image(image)
    oled.show()

    # Wait for the next loop
    time.sleep(LOOPTIME)
