#!/bin/bash


function set_alias() {
  local alias=$1
  local alias_target=$2

  if sudo grep -q "alias $alias=" ~/.bashrc; then
    sed -i "s@alias $alias='.*'@alias $alias=$alias_target@" ~/.bashrc
  else
    echo "alias $alias=$alias_target" >> ~/.bashrc
  fi
}

# smartrack module
# shellcheck source=/dev/null
cd /home/smartrack/smartrack-pi
source .venv/bin/activate
python -m pip install -e .[pi]

# webserver
sudo cp install/nginx/smartrack-settings /etc/nginx/sites-available
sudo ln -s /etc/nginx/sites-available/smartrack-settings /etc/nginx/sites-enabled
sudo systemctl restart nginx


# set alias for smartrack cli
alias="smartrack"
alias_target="/home/smartrack/smartrack-pi/.venv/bin/smartrack"
set_alias "$alias" "$alias_target"


# services
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

#set git
git config --global user.name "Smartrack"
git config --global user.email "Smartrack"
