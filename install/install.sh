#!/bin/bash
function set_config() {
  local line=$1

  if sudo grep -q "$line" /boot/firmware/config.txt; then
    sudo sed -i "s@$line'.*'@$line@" /boot/firmware/config.txt
  else
    sudo sed -i '$a'"$line"'' /boot/firmware/config.txt
  fi
}
function set_alias() {
  local alias=$1
  local alias_target=$2

  if sudo grep -q "alias $alias=" ~/.bashrc; then
    sed -i "s@alias $alias='.*'@alias $alias=$alias_target@" ~/.bashrc
  else
    echo "alias $alias=$alias_target" >> ~/.bashrc
  fi
}

# updates and packages
sudo apt-get update -y
sudo apt-get full-upgrade -y

sudo apt-get -y install python3.11
sudo apt-get -y install python3-pip
sudo apt-get -y install python3.11-venv
sudo apt-get -y install python-is-python3
sudo apt-get -y install i2c-tools libgpiod-dev python3-libgpiod
sudo apt-get -y install nginx

# pi configs
sudo raspi-config nonint do_i2c 0
sudo raspi-config nonint do_spi 0
sudo raspi-config nonint do_ssh 0
sudo raspi-config nonint disable_raspi_config_at_boot 0
set_config "usb_max_current_enable=1"

# network manager interfaces and defaults
sudo nmcli connection delete id ipstatic
sudo nmcli connection delete id dhcp
sudo nmcli c add ifname eth0 type ethernet con-name ipstatic
sudo nmcli c add ifname eth0 type ethernet con-name dhcp
sudo nmcli con mod ipstatic ipv4.method manual ipv4.addresses 192.168.1.241/24 ipv4.gateway 192.168.1.1 ipv4.may-fail no ipv6.method disabled connection.autoconnect no connection.autoconnect-priority -1
sudo nmcli con mod dhcp ipv4.method auto ipv4.addresses '' ipv4.gateway '' ipv4.may-fail no ipv4.dhcp-timeout 20 ipv6.method disabled connection.autoconnect yes connection.autoconnect-priority 10 connection.autoconnect-retries 3
sudo nmcli con down ipstatic
sudo nmcli con up dhcp

# smartrack pi module and webserver
cd /home/smartrack/smartrack-pi/smartrack_pi
python -m venv .venv --system-site-packages
# shellcheck source=/dev/null
source .venv/bin/activate
pip install --upgrade -r requirements.txt

# python script as services
cd /home/smartrack/smartrack-pi
sudo cp install/services/stats.service /etc/systemd/system/stats.service
sudo cp install/services/button.service /etc/systemd/system/button.service
sudo cp install/services/smartrack-settings.service /etc/systemd/system/smartrack-settings.service
sudo systemctl daemon-reload
sudo systemctl enable stats.service
sudo systemctl enable button.service
sudo systemctl enable smartrack-settings.service
sudo systemctl start stats.service
sudo systemctl start button.service
sudo systemctl start smartrack-settings.service

# # webserver
sudo cp install/nginx/smartrack-settings /etc/nginx/sites-available
sudo rm /etc/nginx/sites-enabled/default
sudo ln -s /etc/nginx/sites-available/smartrack-settings /etc/nginx/sites-enabled
sudo systemctl restart nginx

# set alias for smartrack cli
alias="smartrack"
alias_target="'/home/smartrack/smartrack-pi/smartrack_pi/.venv/bin/python /home/smartrack/smartrack-pi/smartrack_pi/cli.py'"
set_alias "$alias" "$alias_target"

#set git
git config --global user.name "Smartrack"
git config --global user.email "Smartrack"

#set companion
sudo cp /home/smartrack/smartrack-pi/companion/db /home/companion/.config/companion-nodejs/v3.2/db
sudo reboot

