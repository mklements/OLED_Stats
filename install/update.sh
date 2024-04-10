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
python -m venv .venv --system-site-packages
# shellcheck source=/dev/null
source .venv/bin/activate
pip install --upgrade -r requirements.txt
chmod 0777 smartrack_pi/config.json # allows webpage to write to config



# webserver

sudo cp install/apache/smartrack-config.conf /etc/apache2/sites-available/smartrack-config.conf
sudo cp install/apache/envvars /etc/apache2/envvars
sudo a2ensite smartrack-config
sudo a2enmod rewrite
sudo a2dissite 000-default
sudo chmod +x /home/smartrack # needed for apache access
sudo service apache2 reload

# set alias for smartrack cli
alias="smartrack"
alias_target="'/home/smartrack/smartrack-pi/.venv/bin/python /home/smartrack/smartrack-pi/smartrack_pi/cli.py'"
set_alias "$alias" "$alias_target"

# services
sudo cp install/stats.service /etc/systemd/system/stats.service
sudo cp install/button.service /etc/systemd/system/button.service

sudo systemctl daemon-reload
sudo systemctl enable stats.service
sudo systemctl enable button.service
sudo systemctl start stats.service
sudo systemctl start button.service