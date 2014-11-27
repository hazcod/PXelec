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


## Annex: Overlay
To boot several OpenELEC systems using the same PXE config file and keep their Storage area separate, use 'disk=NFS=...' and add the 'overlay' option. Each OpenELEC system will create and use a directory on the NFS server named '/export/[MAC-address]'.
Note that overlay mounts currently only work with NFS. In theory it should be possible with CIFS/SMB mounts also, but Busybox 'mount' currently doesn't support mounting subdirectories of SMB shares.

Example (boot from NFS, mount each system's /storage from a unique directory in /var/lib/openelec):
ip=dhcp boot=NFS=192.168.1.1:/tftpboot disk=NFS=192.168.1.1:/var/lib/openelec overlay
We could then copy over our settings.
