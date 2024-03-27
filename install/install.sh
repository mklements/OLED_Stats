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

python -m venv .venv --system-site-packages
source .venv/bin/activate
pip install --upgrade -r requirements.txt

sudo cp install/stats.service /etc/systemd/system/stats.service
sudo cp install/button.service /etc/systemd/system/button.service

sudo systemctl daemon-reload
sudo systemctl enable stats.service
sudo systemctl enable button.service
sudo systemctl start stats.service
sudo systemctl start button.service