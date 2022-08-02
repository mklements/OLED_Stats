# OLED_Stats

OLED Stats Display Script For Raspberry Pi

Full setup instructions available on my blog - https://www.the-diy-life.com/add-an-oled-stats-display-to-raspberry-pi-os-bullseye/
Or my Youtube Channel - https://youtu.be/lRTQ0NsXMuw

The script is pre-configured for 128x64 I2C OLED Display, but can easily be modified to run on a 128x32 I2C OLED Display

## Steps:

1. Connect GND, VCC(3.3v), SCL, & SDA ports of the display according to the picture shown below:

<img src="https://www.the-diy-life.com/wp-content/uploads/2021/11/Screenshot-2021-11-14-at-22.16.39-1024x576.jpg">

2. Upgrade your Raspberry Pi firmware and reboot:

```shell
    $ sudo apt-get update
    $ sudo apt-get full-upgrade
    $ sudo reboot
```

3. Install python3-pip

```shell
$ sudo apt-get install python3-pip
$ sudo pip3 install --upgrade setuptools
```

4. Next, we’re going to install the Adafruit CircuitPython library using the following commands:

```shell
$ cd ~
$ sudo pip3 install --upgrade adafruit-python-shell
$ sudo reboot

$ wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
$ sudo python3 raspi-blinka.py
```