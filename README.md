PXelec
======

Automatic updater for OpenELEC machines that perform PXE booting, written in Python.
For your convenience, you may want this script ran in the same environment as the XBMC SQL server.

PXE booting? [PXE booting is booting from the network without any need for a local disk.](http://wiki.openelec.tv/index.php/Network_Boot_-_NFS)


## Instructions
- python PXelec.py --help
- Configure the script PXelec.sh to run weekly in cron.
- Enjoy!

## Requirements
Python 3.x

## Steps
1. Check for new image on OpenELEC website
2. Download image
3. Unpack to temporary location
4. Ping all clients
5. (if ping successful) Check if there is media being played remotely (JSON)
5. (if ping successful and not busy) Issue shutdown
6. Replace SYSTEM and KERNEL with those from the updated package
7. Issue boot to all clients using WOL
