# CTUS Smartrack

## Install

```
cd ~
sudo rm -d -r smartrack-pi
git clone https://github.com/ctus-dev/smartrack-pi.git
cd smartrack-pi
chmod +x install/install.sh
install/install.sh
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

-   Display Stats

```
smartrack display stats

smartrack display stats false
```

-   Display Message

```
smartrack display message "A Test Message"
```

-   Display Message Multi Line ('+' between lines)

```
smartrack display message "A Test Message+Line 2"
```
