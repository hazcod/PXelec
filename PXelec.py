#!/usr/bin/python
# -*- coding: utf-8 -*-

#  PXelec.py
#  ----------------
#  Compatibility: Python3
#  Usage: run "python PXelec.py" (without the quotes) in terminal
#  Root/Administrator privileges required: no
#  Author: Niels Hofmans (hazcod[|__apostrofe__|]outlook.be)
#  Want to make this better? -> https://github.com/HazCod/PXelec

# imported modules
import re
import os
import sys
import argparse
import stat
import tarfile
import warnings
import time
from XBMC import XBMC
from urllib.request import urlopen, urlretrieve

#== constants and global variables
# The OpenELEC download page. Change to other builds of necessary.
repo='get-openelec/viewcategory/8-generic-builds'
openELEC_url='http://openelec.tv/'

# The Remote login credentials for XBMC, leave empty if unused.
RPC_login="htpc"
RPC_pass ="htpc"

# The port XBMC is listening at
port="8080"

# Log informational messages ?
debugging=True

# Where to temporarily store OpenELEC image
temp="OpenELEC.tar"

# How long should a client receive no input before it's called idle
idle_treshold=120
#==

# Variables
clients = None
versionfile = 'version'
currentversion = 0
versionmatch=r'OpenELEC Stable - Generic x86_64 Version:(\d+\.*\d*\.*\d*)'
dl_url='http://releases.openelec.tv/OpenELEC-Generic.x86_64-'

def log( logmsg ):
# log : with debugging enabled, debug to file and screen!
	if debugging:
		print(logmsg)

def file_test( file ):
# file_test : Give warning when the file doesn't exist or is empty.
	if (0 == os.path.isfile(file) or (0 == os.stat(file)[stat.ST_SIZE])):
		log("Invalid file; " + file + ". Empty?")	
		quit()	
		return 1
	else:
		return 0

def openFile( wfile ):
# openFile : return file contents
	file_test(wfile)
	try:
		f = open(wfile, "r")
		result = f.read()
	finally:
		f.close()
	return result

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def main(argv=None):
# main : This is ran when you start the script.
	#Global vars
	global repo
	global openELEC_url
	global RPC_login
	global RPC_pass
	global port
	global clients
	global versionfile
	global currentversion
	global versionmatch
	global dl_url
	global idle_treshold
	
	clients=None
	warnings.filterwarnings("ignore", category=UserWarning, module='urllib')

	#Commandline parameter handling
	if argv is None:
		parser = argparse.ArgumentParser()
		parser.add_argument("Clientlist", help="File of IP adresses of all OpenELEC clients, one per line.")
		parser.add_argument("Path", help="The path of your OpenELEC XPE boot files (kernel, SYSTEM)")
		parser.add_argument("-l","--login", help="XBMC RPC login user.")
		parser.add_argument("-p","--password", help="XBMC RPC login password.")
		parser.add_argument("-P","--port", help="XBMC RPC login port.")
		parser.add_argument("-v", "--version", help="Version to update to. Leave this empty for the latest one.")
		args = parser.parse_args()
		if (args.Clientlist is not None and args.Path is not None):
			if not (os.path.isfile(args.Clientlist)):
				raise Exception("Clientlist must exist!")
				quit()
			else:
				clients = openFile(args.Clientlist).split("\n")
			if (args.port) and not (int(args.port) <= 0):
				port = args.port
			if (args.login) and not (args.login.trim() == ""):
				RPC_login = args.login
			if (args.password) and not (args.password.trim() == ""):
				RPC_pass = args.password
		else:
			raise Exception("Must provide an argument!")
			Usage()

	#-- Start Script
	# Get current version (if any)
	if not (os.path.isfile(versionfile)):
		try:
			f = open(versionfile, "w")
			f.write("0")
		finally:
			f.close()
	else:
		current = int(openFile(versionfile))

	log("Current version: " + str(currentversion))

	# Get latest version
	repo_source = None;
	repo_source = urlopen(openELEC_url + repo).read().decode('utf-8')
	if (repo_source is None):
		raise Exception("No internet access!")
		quit()
		
	match = re.search(versionmatch, repo_source)
	version = int(match.group(1).replace(".",""))
	log("Latest update: " + match.group(1))
	if (version > currentversion):
		# Update!
		log("Update needed")
		url = dl_url + match.group(1) + '.tar'
		log("Downloading " + url + " to " + temp)
		urlretrieve(url, temp)
		# unpack
		log('Extracting..')
		tar = tarfile.open(temp)
		try:
			tar.extractall()
		finally:
			tar.close()
		# remove tar
		os.remove(temp)
		# change to openelec/target directory
		os.chdir((dl_url + match.group(1)).split('/')[-1] + '/target');
		theClients = []
		for line in clients:
			if (line.strip() != ""):
				xbmc = XBMC('http://' + line.strip() + ':' + port + '/jsonrpc', RPC_login,  RPC_pass)
				if (xbmc.JSONRPC.Ping()['result'] == "pong"):
					log(line.strip() + ' : ONLINE!')
					theClients.append(xbmc)
				else:
					log(line.strip() + " : RPC call failed")
		if (len(theClients) > 0):
			#We have online hosts
			#http://kodi.wiki/view/JSON-RPC_API/v3#JSONRPC.Introspect
			print(xbmc.System.GetProperties({"properties" : ["System.IdleTime"]}))#{ "items": ["System.ScreenSaverActive "] }}))
			#timeIdle = None
			if (timeIdle >= idle_treshold):
				#xbmc.shutdown()
				time.sleep(10)
		else:
			log('No online hosts found')
		
		#TODO: Replace SYSTEM and KERNEL
		
		#TODO: Wake up (WOL?) clients

	else:
		# No update needed
		log("No update needed")


	

#==========================#
#      START MAIN ()	   #
#==========================#
if __name__ == "__main__": #
    sys.exit(main())	   #
#==========================#
