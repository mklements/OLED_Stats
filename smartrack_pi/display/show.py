"""Interface for retreiving stats and displaying on an OLED"""

import subprocess
from pathlib import Path

import adafruit_ssd1306
import board
from PIL import Image, ImageDraw, ImageFont

WIDTH = 128
HEIGHT = 64
FONTSIZE = 16
CHAR_WIDTH = 18


def stats(status=True):
    commands = ["sudo", "systemctl", "start", "stats"]
    if not status:
        commands.remove("start")
        commands.insert(2, "stop")
    return subprocess.run(
        commands,
        check=False,
    )


def split_message(message):
    message_list = message.split(" ")
    output = []
    line = ""
    for i, text in enumerate(message_list):
        new_line = f"{line}{text}"
        # print(text, "|", line, "|", new_line, "|", len(new_line))
        if len(new_line.rstrip()) < CHAR_WIDTH:
            if i == len(message_list) - 1:
                output.append(new_line)
                break
            line = f"{new_line} "
            continue
        if len(new_line.rstrip()) == CHAR_WIDTH:
            output.append(new_line)
            line = ""
            continue
        output.append(line.rstrip())
        if i == len(message_list) - 1:
            output.append(text)
            break
        line = f"{text} "
    if len(output) > 4:
        print("Warning:  Too many lines, truncating")
        output = output[:4]
    return output


def text(message):
    lines = split_message(message)

    stats(False)
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
        f"{Path(__file__).parent.parent / 'assets' / 'fonts' / 'PixelOperator.ttf'}",
        FONTSIZE,
    )
    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)
    for i, line in enumerate(lines):
        draw.text((x, top + i * FONTSIZE), line, font=font, fill=255)
    oled.image(image)
    oled.show()
