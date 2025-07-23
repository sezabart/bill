# Brief
'bill' is a small webapp for the purposes of creating bills.

It is intented as voluntary project to support the Center ROG.

When members at for example the FabLab use material of Center ROG, say 3D printing filament, this has to be payed for at the Center ROG shop.
To facilitate this a small paper bill is handwritten.

This project tries to make this easier by re-using an old phone as a kiosk-style portal where bill information can be filled in, after which the bill gets printed on thermal paper like a receipt.

Current setup is a FastHTML server on an underpowered Orange Pi Zero connected via USB to a TSP100 thermal printer with an old Motorola smartphone running Android as the kiosk for the webpage.

This is a working prototype by Bart Smits, being preformed in spare time in and around Ljubljana. Any help appreciated.

# Project Implementation on Orange Pi Zero

## Prerequisites
- ARM microcomputer (Orange Pi Zero)
- [Armbian Bookworm or better](https://www.armbian.com/orange-pi-zero/)
- Internet connection during installation
- SSH access
- TSP100 Thermal Printer, from step 8 onwards.

## Step-by-Step Implementation


### 1. Initialize system

Install your OS.
Establish SSH connection.
Update the system:
```sh
sudo apt update
sudo apt upgrade -y
```

### 2. Install Required Packages

Install necessary packages to set up python:
```sh
sudo apt install -y git python3 python3-pip python3-venv
sudo apt-get install libxml2-dev libxslt-dev
```

### 3. Clone the Project Repository

Preferably as root in the ~/ directory.
```sh
git clone https://github.com/sezabart/bill
cd bill
```

### 4. Install Virtual Environment and Project Dependencies

```sh
python3 -m venv venv
source venv/bin/activate
```
You might have difficulty with:
- uvloop, might have to skip
- apsw, takes long
- relatorio, just takes long


### 5. Enable Autostart (Optional)

To run your project on boot, you can create a systemd service:
```sh
sudo nano /etc/rc.local

```
Add the following content between the comments and `exit 0`
```sh
(
  cd /root/bill
  venv/bin/python server.py
)
```
Adjust the permissions to allow the rc.local 'user' to run the server.
```sh
chmod -R 7445 /root/bill/
```

### 8. Install CUPS

```sh
sudo apt install cups libcups2-dev
sudo cupsctl --remote-any
sudo /etc/init.d/cups restart
```

### 9. Clone drivers for thermal printer

```sh
git clone https://github.com/sezabart/TSP100-Ubuntu-Debian-driver
cd TSP100-Ubuntu-Debian-driver
```
Compile and install driver 
Replace XXX with the version, use `tab` to have it autocomplete.
```sh
tar -zxvf Star-CUPS-Driver-src-XXX.tar.gz
cd Star-CUPS-Driver
sudo make
sudo make install
```

### 10. Install driver

```sh
sudo chmod +X star-cups-driver_......
sudo dpkg -i star-cups-driver_....
```

### 11. Configure CUPS

You should now be able to navigate to `192.168.<your subnet>.<the server>:631` and see the CUPS interface.
Go to Administration and Add printer

If you aren't currently connected to the printer, use the any option and fill in:
`usb://Star/TSP143%20(STR_T-001)`
Continue and give your printer a good name, description and location.
Continue and choose 'STAR' and for model choose 'Star TSP100 <Cutter or Tearbar, depending on what you have>'

### 12. Run project
```sh
cd ~/bill
python server.py
```
You should now have bill running on `192.168.<your subnet>.<the server>:5001`
Print jobs should print, consult the CUPS page otherwise, to see where it goes wrong.

### 13. Profit?

## Maintenance

### VPN

VPN is setup on the board using wireguard
`sudo apt install wireguard`

Then copy your conf to `/etc/wireguard` directory and name it something simple like `wg.conf`.
Edit it to add PostUp functionality to make add the IP route every time:
```sh
[Interface]
PrivateKey = ...
Address = 192.168.<n>.<m>/24
PostUp = ip route add 192.168.<n>.0/24 dev wg (.conf)
PostDown = ip route del 192.168.<n>.0/24 dev wg

[Peer]
PublicKey = ...
Endpoint = ...
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25
```



