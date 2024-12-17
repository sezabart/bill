# Project Implementation on Raspberry Pi 3B+

## Prerequisites
- Raspberry Pi 3B+
- RPi OS Bookworm 32-bit Lite installed
- Internet connection
- SSH access (optional but recommended)
- TSP100 Thermal Printer, from step 8 onwards.

## Step-by-Step Implementation

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
pip install -r requirements.txt
```

### 5. Enable Autostart (Optional)

To run your project on boot, you can create a systemd service:
```sh
sudo nano /etc/systemd/system/bill.service

```
Add the following content, replacing placeholders with your project details:
```ini
[Unit]
Description=bill

[Service]
ExecStartPre=/usr/bin/apt update
ExecStartPre=/usr/bin/apt upgrade -y
ExecStartPre=/usr/bin/git -C /home/<user>/bill pull
ExecStartPre=/bin/bash -c 'source /home/<user>/bill/venv/bin/activate'
ExecStart=/bin/bash -c 'source /home/<user>/bill/venv/bin/activate && python /home/<user>/bill/server.py'
WorkingDirectory=/home/<user>/bill
Restart=always
User=<user>

[Install]
WantedBy=multi-user.target
```
Enable the service:
```sh
sudo systemctl enable bill.service
sudo systemctl start bill.service
```

### 8. Clone drivers for thermal printer

```sh
git clone https://github.com/sezabart/TSP100-Ubuntu-Debian-driver
cd TSP100-Ubuntu-Debian-driver
```

### 9. Install driver

```sh
sudo chmod +X star-cups-driver_......
sudo dpkg -i star-cups-driver_....
```
Auto-complete using `tab` is your friend.

### 10. Install CUPS

```sh
sudo apt install cups
```
If you are able to visit the webpage locally, proceed to 11. 
Else to configure over the network, we need to allow access.

 TODO: add file to repo 
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