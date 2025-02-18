# Project Implementation on Orange Pi Zero

## Prerequisites
- ARM mi
- Armbian Bookworm or better
- Internet connection during installation
- SSH access
- TSP100 Thermal Printer, from step 8 onwards.

## Step-by-Step Implementation

### 0. Install your OS and establish SSH connection

### 1. Update and Upgrade the System

```sh
sudo apt update
sudo apt upgrade -y
```

### 2. Install Required Packages

Install necessary packages for your project. For example:
```sh
sudo apt install -y git python3 python3-pip python3-venv
sudo apt install -y libreoffice-writer-nogui
```
That last one is big and might take a while.

### 3. Clone the Project Repository

```sh
git clone https://github.com/sezabart/bill
cd bill
```

### 4. Install Virtual Environment and Project Dependencies

```sh
python3 -m venv venv
source venv/bin/activate
```
Dont install uvloop
apsw takes a looong time
relatatorio takes a loooong time

```sh
pip install apsw==3.44.2.0 --no-cache-dir --no-binary apsw

sudo apt-get install libxml2-dev libxslt-dev

pip install relatorio

pip install python-fasthtml
```

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
Adjust the permissions.
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
Auto-complete using `tab` is your friend.



Copy over the conf
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

## Conclusion
Your project should now be running on the Raspberry Pi 3B+ with RPi OS Bookworm 32-bit Lite. Ensure to monitor the logs and performance to make any necessary adjustments.