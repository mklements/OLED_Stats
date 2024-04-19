"""Interface for retreiving stats and displaying on an OLED"""

import json
import os
import socket
import time
from pathlib import Path

import adafruit_ssd1306
import board
import psutil as ps
from PIL import Image, ImageDraw, ImageFont

KB = 1024
MB = KB * 1024
GB = MB * 1024

WIDTH = 128
HEIGHT = 64
FONTSIZE = 16

LOOPTIME = 1.0

dir_path = os.path.dirname(os.path.realpath(__file__))


def get_config():
    with open(f"{dir_path}/net/config.json", encoding="utf-8") as f:
        return json.load(f)


def get_ip():
    """Returns the IP from a specific interface"""
    try:
        iface = ps.net_if_addrs()["eth0"]
        for addr in iface:
            if addr.family is socket.AddressFamily.AF_INET:
                return f"IP: {addr.address}"
    except Exception:
        return "IP: ???:???:???:???"


def get_hostname():
    return socket.gethostname()


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
bottom = oled.height - padding
x = 0

# font = ImageFont.load_default()
font = ImageFont.truetype(
    f"{Path(__file__).parent / 'assets' / 'fonts' / 'PixelOperator.ttf'}", FONTSIZE
)

count = 0

while True:
    config = get_config()
    title = ""
    count += 1
    if 1 <= count <= 3:
        title = get_hostname()
    elif 4 <= count <= 6:
        title = get_ip()

    if count == 6:
        count = 0

    cpu = f"CPU: {ps.cpu_percent():.1f} %"

    temps = ps.sensors_temperatures()
    temp = f"{temps['cpu_thermal'][0].current:.1f} °C"

    mem = ps.virtual_memory()
    mem_usage = f"Mem: {(mem.used+GB-1)/GB:.1f}/ {round((mem.total+GB-1)/GB):.1f} GB"

    root = ps.disk_usage("/")
    disk = f"Disk: {(root.used+GB-1)/GB:.1f}/ {(root.total+GB-1)/GB:.1f} GB"

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)
    draw.text((x, top), title, font=font, fill=255)
    draw.text((x + 118, top), config.get("mode", "!"), font=font, fill=255)
    draw.text((x, top + FONTSIZE), cpu, font=font, fill=255)
    draw.text((x + 80, top + FONTSIZE), temp, font=font, fill=255)
    draw.text((x, top + 2 * FONTSIZE), mem_usage, font=font, fill=255)
    draw.text((x, top + 3 * FONTSIZE), disk, font=font, fill=255)

    # Display image
    oled.image(image)
    oled.show()
    time.sleep(LOOPTIME)
