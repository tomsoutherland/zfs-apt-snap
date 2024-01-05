# zfs-apt-snap

This is a simple python script to manage snapshots when apt/nala/dpkg is ran to add/remove packages.  
This script assumes all datasets associated with the boot disk are contained within the mounted  
root ( / ) dataset. If this is not your setup, this script is not for you without modifications.  

There is no install script but installation is simple.

  1. copy 80snapshotconf to /etc/apt/apt.conf.d/80snapshotconf  
  2. copy zfs-apt-snap.py to /usr/local/sbin/zfs-apt-snap.py  
        $ cp zfs-apt-snap.py /usr/local/sbin/zfs-apt-snap.py  
        $ chmod +x /usr/local/sbin/zfs-apt-snap.py  

There are a couple of items you man wish to tune in the zfs-apt-snap.py script.  
  1. SNAPPURGE = 5  # delete snapshots older than SNAPPURGE days  
  2. SNAPSKIP = 120 # prevent new snaps if last snap is less than SNAPSKIP seconds  
