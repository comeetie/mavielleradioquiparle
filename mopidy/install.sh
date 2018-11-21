#! /bin/sh
cp rotary_volume.py /usr/local/bin/
sudo cp rotary_volume.sh /etc/init.d/
sudo update-rc.d rotary_volume.sh defaults
cp rotary_stations.py /usr/local/bin
sudo cp rotary_stations.sh /etc/init.d/
sudo update-rc.d rotary_stations.sh defaults
cp led.py /usr/local/bin
sudo cp led.sh /etc/init.d/
sudo update-rc.d led.sh defaults



