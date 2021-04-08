Connect to ```rpi-config-ap``` using password ```password```.

Logger server on self-hosted access point is at http://192.168.88.1

Server will be available around 30 seconds after the Pi is connected to power.

### Configure Startup Scripts
* Run ```sudo crontab -e``` using nano.
* Add the line ```@reboot cd /home/pi/yada-logger && sudo /usr/local/bin/node server.js &```
