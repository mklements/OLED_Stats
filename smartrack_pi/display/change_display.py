"""Interface for retreiving stats and displaying on an OLED"""

import os
import subprocess
import sys
from pathlib import Path

import adafruit_ssd1306
import board
import psutil as ps
from PIL import Image, ImageDraw, ImageFont

WIDTH = 128
HEIGHT = 64
FONTSIZE = 16


def stats_status(status=True):
    commands = ["sudo", "systemctl", "start", "stats"]
    if not status:
        commands.remove("start")
        commands.insert(2, "stop")
    return subprocess.run(
        commands,
        check=False,
    )


def display_text(*messages):
    stats_status(False)
    i2c = board.I2C()
    oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C)
    oled.fill(0)
    oled.show()
    image = Image.new("1", (oled.width, oled.height))
    draw = ImageDraw.Draw(image)

    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)
    padding = -2
    top = padding
    bottom = oled.height - padding
    x = 0

    # font = ImageFont.load_default()
    font = ImageFont.truetype(
        f"{Path(__file__).parent.parent / 'fonts' / 'PixelOperator.ttf'}", FONTSIZE
    )
    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)
    for i, line in enumerate(messages):
        draw.text((x, top + i * FONTSIZE), line, font=font, fill=255)
    oled.image(image)
    oled.show()
