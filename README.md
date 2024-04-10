# CTUS Smartrack

## Install

```
cd ~
git clone https://github.com/ctus-dev/smartrack-pi.git
cd smartrack-pi
chmod +x install/install.sh
install/install.sh
```

### Update

```
smartrack display message "Updating..."
sudo systemctl stop stats.service
sudo systemctl stop button.service
cd ~
sudo rm -d -r smartrack-pi
git clone https://github.com/ctus-dev/smartrack-pi.git
cd smartrack-pi
chmod +x install/update.sh
install/update.sh
```

### Post install or update

```
sudo reboot
```

## Operation

### CLI

-   Network Mode

```
smartrack dhcp

smartrack static 192.168.1.100 192.168.1.1
```

- Display Stats (true or false)

```
smartrack display stats true
```

- Display Message

```
smartrack display message "A Test Message"
```