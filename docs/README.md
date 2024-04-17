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

- Software Update
```
smartrack update
```

- Factory Reset
```
smartrack factory
```

### Companion Config

Database is contained at /home/companion/.config/companion-nodejs/v3.2/db (note the version number if image changes).  This command will copy the current config 

## Notes

- If companion image changes database folder needs to be changed in install.sh