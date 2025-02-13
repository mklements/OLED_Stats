# Created by: Michael Klements
# For Raspberry Pi Desktop Case with OLED Stats Display & SupTronics X1200 UPS
# Base on Adafruit Blinka & SSD1306 Libraries
# Installation & Setup Instructions - https://www.the-diy-life.com/add-an-oled-stats-display-to-raspberry-pi-os-bullseye/
import time
import board
import busio
import gpiozero
import struct
import smbus
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import subprocess

# Define the Reset Pin using gpiozero
oled_reset = gpiozero.OutputDevice(4, active_high=False)  # GPIO 4 (D4) used for reset

# Display Parameters
WIDTH = 128
HEIGHT = 64
BORDER = 5

# Switch between displays every 5 seconds
LOOPTIME = 5.0

i2c = board.I2C()
oled_reset.on()
time.sleep(0.1)
oled_reset.off()
time.sleep(0.1)
oled_reset.on()

oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C)

oled.fill(0)
oled.show()

width = oled.width
height = oled.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
padding = -2
top = padding
x = 0

font = ImageFont.truetype('PixelOperator.ttf', 16)
icon_font = ImageFont.truetype('lineawesome-webfont.ttf', 18)

# UPS Setup
bus = smbus.SMBus(1)
address = 0x36

# Get UPS parameters
def readVoltage():
    read = bus.read_word_data(address, 2)
    swapped = struct.unpack("<H", struct.pack(">H", read))[0]
    return swapped * 1.25 / 1000 / 16

def readCapacity():
    read = bus.read_word_data(address, 4)
    swapped = struct.unpack("<H", struct.pack(">H", read))[0]
    return swapped / 256

def get_ups_status(voltage, ac_power):
    return "Plugged In" if ac_power else "Power Loss"

display_mode = 0  # Toggle between 0 (System Stats) and 1 (UPS Info)

# GPIO pin 6 used for power status detection
ups_power_status_pin = gpiozero.DigitalInputDevice(6)  

while True:
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    if display_mode == 0:
        # System Stats Screen
        IP = subprocess.check_output("hostname -I | cut -d' ' -f1", shell=True).strip().decode()
        CPU = subprocess.check_output("top -bn1 | grep load | awk '{printf \"%.2fLA\", $(NF-2)}'", shell=True).strip().decode()
        MemUsage = subprocess.check_output("free -m | awk 'NR==2{printf \"%.2f%%\", $3*100/$2 }'", shell=True).strip().decode()
        Disk = subprocess.check_output("df -h | awk '$NF==\"/\"{printf \"%d/%dGB\", $3,$2}'", shell=True).strip().decode()
        Temperature = subprocess.check_output("vcgencmd measure_temp | cut -d '=' -f2", shell=True).strip().decode()

        draw.text((x, top + 5), chr(62609), font=icon_font, fill=255)
        draw.text((x + 65, top + 5), chr(62776), font=icon_font, fill=255)
        draw.text((x, top + 25), chr(63426), font=icon_font, fill=255)
        draw.text((x + 65, top + 25), chr(62171), font=icon_font, fill=255)
        draw.text((x, top + 45), chr(61931), font=icon_font, fill=255)

        draw.text((x + 19, top + 5), Temperature, font=font, fill=255)
        draw.text((x + 87, top + 5), MemUsage, font=font, fill=255)
        draw.text((x + 19, top + 25), Disk, font=font, fill=255)
        draw.text((x + 87, top + 25), CPU, font=font, fill=255)
        draw.text((x + 19, top + 45), IP, font=font, fill=255)
    
    else:
        # UPS Info Screen
        voltage = readVoltage()
        capacity = readCapacity()
        
        ac_power = ups_power_status_pin.is_active  # Check if the GPIO pin for UPS status is high (plugged in)
        ups_status = get_ups_status(voltage, ac_power)

        ups_icon = chr(61926) if ac_power else chr(0xf071)
        battery_icon = chr(62018) if capacity > 50 else chr(62020)
        bolt_icon = chr(61671)

        draw.text((x + 10, top + 5), ups_icon, font=icon_font, fill=255)
        draw.text((x + 35, top + 5), ups_status, font=font, fill=255)

        draw.text((x + 20, top + 25), battery_icon, font=icon_font, fill=255)
        draw.text((x + 45, top + 25), f"{capacity:.1f}%", font=font, fill=255)

        draw.text((x + 20, top + 45), bolt_icon, font=icon_font, fill=255)
        draw.text((x + 45, top + 45), f"{voltage:.2f}V", font=font, fill=255)
    
    oled.image(image)
    oled.show()
    
    time.sleep(LOOPTIME)
    display_mode = 1 - display_mode
