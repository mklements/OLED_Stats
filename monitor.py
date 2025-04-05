import time
import board
import busio
import digitalio
import smbus
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import subprocess

# Display Parameters
WIDTH = 128
HEIGHT = 64
BORDER = 5
LOOPTIME = 1.0

# Use for I2C
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C)

# Clear display
oled.fill(0)
oled.show()

# Create blank image for drawing
width = oled.width
height = oled.height
image = Image.new('1', (width, height))

# Get drawing object
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image
draw.rectangle((0, 0, width, height), outline=0, fill=0)

# First define some constants to allow easy resizing of shapes
padding = -2
top = padding
bottom = height - padding
x = 0

# Load default font
font = ImageFont.load_default()

# Alternatively, load a TTF font
font = ImageFont.truetype('PixelOperator.ttf', 14)
icon_font = ImageFont.truetype('lineawesome-webfont.ttf', 16)

# Battery Address and low voltage threshold
ADDR = 0x2d
LOW_VOL = 3150  # mV

# Initialize I2C bus
bus = smbus.SMBus(1)

charging_animation_stage = 0  # Track animation stage for charging

def get_battery_status():
    """
    Read battery status and return the icon value and percentage.
    """
    # Read battery data
    data = bus.read_i2c_block_data(ADDR, 0x20, 0x0C)
    current = (data[2] | data[3] << 8)
    if current > 0x7FFF:
        current -= 0xFFFF
    battery = int(data[4] | data[5] << 8)

    # Read battery status
    data = bus.read_i2c_block_data(ADDR, 0x02, 0x01)
    bat_icon = 0xf244  # Default battery icon

    is_charging = data[0] & 0x40 or data[0] & 0x80

    if is_charging:
        if battery == 100:
            bat_icon = 0xf240  # Fully charged icon
        else:
            bat_icon = 0xf244  # Charging icon
    else:
        if battery == 100:
            bat_icon = 0xf240  # Fully charged icon
        elif battery >= 50:
            bat_icon = 0xf242  # 50-100% icon
        elif battery >= 25:
            bat_icon = 0xf243  # 25-50% icon
        else:
            bat_icon = 0xf244  # Less than 25% icon

    return bat_icon, battery, is_charging

def animate_charging():
    """
    Animate the charging icon by cycling through different stages.
    """
    # Define charging stages (icons for 0%, 25%, 50%, 75%, 100% charging)
    charging_icons = [0xf244, 0xf243, 0xf242, 0xf241, 0xf240]
    return charging_icons


def boot_animation():
    icon_font = ImageFont.truetype('lineawesome-webfont.ttf', 46)
    # Icon (0xf7b9) - Replace this with the character or icon you want to display
    icon = 0xf7b9
    """
    Display a rotating animation during boot.
    """
    for i in range(36):  # Loop to rotate the icon 36 times (360 degrees total)
        # Clear the display
        draw.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0)
        
        # Draw the rotating icon
        draw.text((WIDTH // 2 - 8, HEIGHT // 2 - 8), chr(icon), font=icon_font, fill=255)

        # Rotate the image by 10 degrees (small increment)
        image_rotated = image.rotate(i*10, expand=True)

        # Resize the rotated image back to 128x64 (screen size)
        image_resized = image_rotated.resize((WIDTH, HEIGHT))

        # Display the rotated image on the OLED screen
        oled.image(image_resized)
        oled.show()

        # Wait for a short time before rotating again
        time.sleep(0.5)


# Boot animation sequence
boot_animation()

while True:
    # Get battery status and icon
    bat_icon, battery, is_charging = get_battery_status()

    # Clear the display
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Get system information using subprocess
    cmd = "hostname -I | cut -d' ' -f1 | head --bytes -1"
    IP = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()

    cmd = "top -bn1 | grep load | awk '{printf \"%.2fLA\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()

    cmd = "free -m | awk 'NR==2{printf \"%.2f%%\", $3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()

    cmd = "df -h | awk '$NF==\"/\"{printf \"%d/%dGB\", $3,$2}'"
    Disk = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()

    cmd = "vcgencmd measure_temp | cut -d '=' -f 2 | head --bytes -1"
    Temperature = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()

    # Icons
    draw.text((x, top + 5), chr(62609), font=icon_font, fill=255)  # Icon for temperature
    draw.text((x + 65, top + 5), chr(62776), font=icon_font, fill=255)  # Icon for memory
    draw.text((x, top + 25), chr(63426), font=icon_font, fill=255)  # Icon for disk
    draw.text((x + 65, top + 25), chr(62171), font=icon_font, fill=255)  # Icon for CPU
    draw.text((x, top + 45), chr(61931), font=icon_font, fill=255)  # Icon for wifi
    # Battery icon handling
    if is_charging:
        # Animate the charging icon if the battery is charging
        charging_icons = animate_charging()
        bat_icon = charging_icons[charging_animation_stage]
        charging_animation_stage = (charging_animation_stage + 1) % len(charging_icons)  # Cycle through the icons
    else:
        # If not charging, show the current battery icon
        pass
    draw.text((x + 80, top + 45), chr(bat_icon), font=icon_font, fill=255)  # Icon for battery

    # Text
    draw.text((x + 16, top + 5), str(Temperature), font=font, fill=255)
    draw.text((x + 85, top + 5), str(MemUsage), font=font, fill=255)
    draw.text((x + 16, top + 25), str(Disk), font=font, fill=255)
    draw.text((x + 85, top + 25), str(CPU), font=font, fill=255)
    draw.text((x + 16, top + 45), str(IP), font=font, fill=255)
    draw.text((x + 96, top + 45), f'{battery:.1f}%', font=font, fill=255)

    # Display the image on the OLED
    oled.image(image)
    oled.show()

    # Wait before refreshing the display
    time.sleep(LOOPTIME)
