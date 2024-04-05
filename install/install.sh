#!/bin/bash
function set_config() {
  local line=$1

  if sudo grep -q "$line" /boot/config.txt; then
    sudo sed -i "s@$line'.*'@$line@" /boot/config.txt
  else
    sudo sed -i '$a'"$line"'' /boot/config.txt
  fi
}

set_config "usb_max_current_enable=1"

sudo apt-get update -y
sudp apt-get full-upgrade -y

sudo apt-get -y install python3.11
sudo apt-get -y install python3-pip
sudo apt-get -y install python3.11-venv
sudo apt-get -y install python-is-python3

sudo apt-get -y install  i2c-tools libgpiod-dev python3-libgpiod

sudo raspi-config nonint do_i2c 0
sudo raspi-config nonint do_spi 0
sudo raspi-config nonint do_ssh 0
sudo raspi-config nonint disable_raspi_config_at_boot 0

sudo nmcli c add ifname eth0 type ethernet con-name ipstatic
sudo nmcli c add ifname eth0 type ethernet con-name dhcp
sudo nmcli con mod ipstatic ipv4.method manual ipv4.addresses 192.168.1.241/24 ipv4.gateway 192.168.1.1 ipv4.may-fail no ipv6.method disabled connection.autoconnect no connection.autoconnect-priority -1
sudo nmcli con mod dhcp ipv4.method auto ipv4.addresses '' ipv4.gateway '' ipv4.may-fail no ipv4.dhcp-timeout 20 ipv6.method disabled connection.autoconnect no connection.autoconnect-priority -1 connection.autoconnect-retries 3

python -m venv .venv --system-site-packages
source .venv/bin/activate
pip install --upgrade -r requirements.txt
sudo chown smartrack:smartrack smartrack_pi/.env

sudo cp install/stats.service /etc/systemd/system/stats.service
sudo cp install/button.service /etc/systemd/system/button.service

sudo systemctl daemon-reload
sudo systemctl enable stats.service
sudo systemctl enable button.service
sudo systemctl start stats.service
sudo systemctl start button.service

# webserver
sudo apt-get -y install apache2
sudo apt-get -y install php

sudo cp install/apache/smartrack-config.conf /etc/apache2/sites-available/smartrack-config.conf
sudo cp install/apache/envvars /etc/apache2/envvars
sudo a2ensite smartrack-config
sudo a2enmod rewrite
sudo a2dissite 000-default

chmod +x /home/smartrack
chmod 0777 /home/smartrack/smartrack_pi/.env

sudo service apache2 reload