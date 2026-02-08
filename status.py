#!/usr/bin/env python3
# Created by: Michael Klements & Macley(kun)
# For Raspberry Pi Desktop Case with OLED Stats Display
# Base on Adafruit CircuitPython & SSD1306 Libraries
# Installation & Setup Instructions - https://www.the-diy-life.com/add-an-oled-stats-display-to-raspberry-pi-os-bullseye/
import os, sys, time, atexit, signal
import board, digitalio
import adafruit_ssd1306

from PIL import Image, ImageDraw, ImageFont

import psutil
import socket

WIDTH, HEIGHT = 128, 64
FONT_SZ = 16

oled = adafruit_ssd1306.SSD1306_I2C(
    WIDTH, HEIGHT, board.I2C(), addr=0x3C, reset=digitalio.DigitalInOut(board.D4)
)

rotation = int(os.environ.get("OLED_ROTATION", "1"))
if rotation == 2:
    try:
        oled.rotate(2)
    except AttributeError:
        oled.rotation = 2

def cleanup():
    try:
        oled.fill(0)
        oled.show()
    except Exception:
        pass

def kill_handler(*_):
    cleanup()
    sys.exit(0)

atexit.register(cleanup)
signal.signal(signal.SIGINT, kill_handler)
signal.signal(signal.SIGTERM, kill_handler)

oled.fill(0)
oled.show()

image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)

font = ImageFont.truetype("PixelOperator.ttf", FONT_SZ)
icon_font = ImageFont.truetype("lineawesome-webfont.ttf", FONT_SZ)

# Helper: get a “best guess” LAN IP without shelling out
def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "0.0.0.0"

def get_temp_c():
    # Pi exposes temperature here (on typical Raspberry Pi OS)
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            return float(f.read().strip()) / 1000.0
    except Exception:
        return 0.0

def format_uptime(seconds):
    minutes = seconds // 60
    hours = minutes // 60
    days = hours // 24

    minutes %= 60
    hours %= 24

    if days > 0:
        return f"{days}d {hours}h"
    elif hours > 0:
        return f"{hours}:{minutes:02d}"
    else:
        return f"{minutes}m"

# Cache slow-ish values
ip = get_ip()
last_ip_check = 0.0

last_frame = None

# Prime psutil CPU sampling (first call can be 0.0)
psutil.cpu_percent(interval=None)

while True:
    now = time.time()

    # Refresh IP only every 60s
    if now - last_ip_check > 60:
        ip = get_ip()
        last_ip_check = now

    cpu = psutil.cpu_percent(interval=None)

    vm = psutil.virtual_memory()
    mem_used_gb = vm.used / (1024**3)
    mem_total_gb = vm.total / (1024**3)
    mem_pct = vm.percent

    du = psutil.disk_usage("/")
    disk_pct = du.percent

    uptime_s = int(time.time() - psutil.boot_time())
    uptime = format_uptime(uptime_s)

    temp_c = get_temp_c()

    # Build frame text. If it didn't change, skip OLED update.
    frame = (ip, round(cpu, 0), round(temp_c, 1), round(mem_pct, 1),
             round(mem_used_gb, 1), round(mem_total_gb, 0), int(disk_pct), uptime)

    if frame != last_frame:
        draw.rectangle((0, 0, oled.width, oled.height), fill=0)

        # icons
        draw.text((1, 0),  chr(61931), font=icon_font, fill=255)  # wifi
        draw.text((1, 16), chr(62171), font=icon_font, fill=255)  # cpu
        draw.text((111,16),chr(62153), font=icon_font, fill=255)  # temp
        draw.text((1, 32), chr(62776), font=icon_font, fill=255)  # memory
        draw.text((1, 48), chr(63426), font=icon_font, fill=255)  # disk
        draw.text((111,48),chr(62034), font=icon_font, fill=255)  # time

        # text
        draw.text((22, 0),  ip, font=font, fill=255)
        draw.text((22, 16), f"{cpu:.0f}%", font=font, fill=255)
        draw.text((107,16), f"{temp_c:.1f}°C", font=font, fill=255, anchor="ra")
        draw.text((22, 32), f"{mem_pct:.0f}%", font=font, fill=255)
        draw.text((125,32), f"{mem_used_gb:.1f}/{mem_total_gb:.0f}G", font=font, fill=255, anchor="ra")
        draw.text((22, 48), f"{disk_pct:.0f}%", font=font, fill=255)
        draw.text((107,48), uptime, font=font, fill=255, anchor="ra")

        oled.image(image)
        oled.show()
        last_frame = frame

    time.sleep(5.0)
