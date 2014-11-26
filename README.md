PXelec
======

Automatic updater for OpenELEC machines that perform PXE booting.
For your convience, you may want this script ran in the same environment as the XBMC SQL server.

PXE booting? [PXE booting is booting from the network without any need for a local disk.](http://wiki.openelec.tv/index.php/Network_Boot_-_NFS)


## Instructions
- Add your OpenELEC client IPs in the settings file.
- Configure the script PXelec.sh to run weekly.
- Enjoy!

## Steps
1. Check for new image on OpenELEC website
2. Download image
3. Unpack to temporary location
4. Ping all clients
4. (if ping successful) SSH to all clients with default openelec details
5. (if ping successful) Check if there is media being played using JSON or whatever
5. (if ping successful and not busy) Issue shutdown
6. Replace SYSTEM and KERNEL with those from the updated package
7. Issue boot to all clients
