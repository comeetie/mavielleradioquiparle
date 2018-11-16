#! /bin/sh
cp addplaylist.js /volumio/app/plugins/system_controller/volumio_command_line_client/commands/
cp rotary_volume.py /usr/local/bin/
cp rotary_volume.sh /etc/init.d/
update-rc.d rotary_volume.sh defaults
cp rotary_stations.py /usr/local/bin
cp rotary_stations.sh /etc/init.d/
update-rc.d rotary_stations.sh defaults
cp led.py /usr/local/bin
cp led.sh /etc/init.d/
update-rc.d led.sh defaults
cp startup-serv.sh /etc/init.d/
update-rc.d startup-serv.sh defaults
apt-get update
apt-get install pip 
apt-get install -y cron 
pip install simplejson 
pip install spotipy
apt-get install pico2wav
(crontab -l ; echo "0 3 * * * /home/volumio/build_playlists.py") | sort - | uniq - | crontab -

