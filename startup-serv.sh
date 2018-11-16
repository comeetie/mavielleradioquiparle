#! /bin/sh

### BEGIN INIT INFO
# Provides:          startup.py
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
### END INIT INFO

# If you want a command to always run, put it here

# Carry out specific functions when asked to by the system
case "$1" in
  start)
    echo "Starting"
    /usr/local/bin/startup.sh &
    ;;
  stop)
    echo "Stopping"
    pkill -f /usr/local/bin/startup.py
    ;;
  *)
    echo "Usage: /etc/init.d/rotary.sh {start|stop}"
    exit 1
    ;;
esac

exit 0
