Connect to ```rpi-config-ap``` using password ```password```.

Logger server on self-hosted access point is at http://192.168.88.1

Access point will be available around 60 seconds after the Pi is connected to power.

## Configure Raspberry Pi From Base Image.

### Get Base Image
* Go to https://www.raspberrypi.org/software/operating-systems/ and download the latest Rasperry Pi OS Lite image.
* Flash the image to a microSD card.
* Don't remove the microSD card!

### Configure Pi USB Ethernet Gadget
* With the microSD card still in the machine we flashed from.
* Navigate to the root level of the microSD card.
* Edit ```config.txt``` and add ```dtoverlay=dwc2``` as the last line.
* Edit ```cmdline.txt``` after the word **rootwait** add a space and then ```modules-load=dwc2,g_ether```
* Create a new empty file named ```ssh``` with no extention.
* Now when the Pi is connected to a machine via USB we can SSH into it at ```raspberrypi.local```
* **NOTE** Windows users may need to add Bonjour support so it knows what to do with .local names.  The easiest way to do this is to install iTunes.  More information here https://learn.adafruit.com/bonjour-zeroconf-networking-for-windows-and-linux/.

### Give the Pi Internet Access
* Connect the Pi to the host machine.
* In the system settings of the host machine, bridge a network adapter with internet access and the usb ethernet adapter that is presented from the Pi.
* Now SSH into the Pi and test the network connectivity by trying ```ping 8.8.8.8``` (Google's DNS).
* **NOTE** default SSH credentials are user:```pi``` and password:```raspberry``` 

### Install Dependencies
* Update package list with ```sudo apt-get update```.
* Install **hostapd** with ```sudo apt-get install hostapd```.
* Install **dhcpcd** with ```sudo apt-get install dhcpcd```.
* Install **git** with ```sudo apt-get install git```.
* Enable the NodeSource repository by running ```curl -sL https://deb.nodesource.com/setup_10.x | sudo bash -```.
* Update package list with ```sudo apt-get update```.
* Install Node.js and npm with ```sudo apt-get install nodejs```.

### Clone Repository and Install Node Packages
* SSH into the Pi and navigate into ```/home/pi``` if you're not there already.
* Clone the yada-logger repository with ```git clone https://github.com/Yet-Another-Data-Aggregator/yada-logger.git```.
* CD into the ```yada-logger``` folder.
* Get the needed packages with ```npm install```.

### Install Python Packages
* Install pip3 with ```sudo apt-get install python3-pip```
* Navigate to ```/home/pi/yada-logger/src'''
* Install firebase_admin with ```python3 -m pip install firebase_admin```

### Configure Startup Scripts
* Run ```sudo crontab -e``` using nano.
* Add the line ```@reboot cd /home/pi/yada-logger && sudo /usr/local/bin/node server.js &```
* Add the line ```@reboot cd /home/pi/yada-logger/src && sudo /usr/bin/python3 main.py &```
