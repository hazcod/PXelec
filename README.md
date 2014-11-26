PXelec
======

Automatic updater for OpenELEC machines that perform PXE booting.


Steps:
1. check for new image on OpenELEC website
2. download image
3. unpack to temporary location
5. SSH to all clients with default openelec details
5.1. Issue shutdown to all clients
7. replace SYSTEM and KERNEL with those from the updated package
8. Issue boot to all cients
