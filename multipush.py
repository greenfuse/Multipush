#!/usr/bin/env python3

import os
import getpass
import socket

import appdirs
import yaml

import keyhandling

homedir = os.path.expanduser("~")
user_config = appdirs.user_config_dir()
username = getpass.getuser()
hostname = socket.gethostname()
comment = "multipush-" + username + "@" + hostname

user_app_dir = os.path.join(user_config, "multipush")
key_dir = os.path.join(user_app_dir, "keys")
prvkeypath = os.path.join(key_dir, "id_rsa")
pubkeypath = os.path.join(key_dir, "id_rsa.pub")
# check if private and public keys are present on local client
# filepaths are .config/multipush/keys/keyname


if not os.path.exists(key_dir):
    os.makedirs(key_dir)
    os.chmod(user_app_dir, 0o700)
    os.chmod(key_dir, 0o700)
    keyhandling.makenewkeys(prvkeypath, pubkeypath)
elif not os.path.exists(prvkeypath):
    keyhandling.makenewkeys(prvkeypath, pubkeypath)
elif not os.path.exists(pubkeypath):
    keyhandling.makepubkey(prvkeypath, pubkeypath)

# get list of computernames
# need dialog to prompt for computers if file is not present
# option for scan using nmap-python would be nice
# https://www.studytonight.com/network-programming-in-python/integrating-port-scanner-with-nmap
# https://xael.org/pages/python-nmap-en.html

computerfile = os.path.join(user_app_dir, "computers.yml")
with open(computerfile, 'r') as stream:
    computerlists = yaml.safe_load(stream)

# for testing - later make it user select
testcomputers = computerlists['Test Computers']
computer = testcomputers[0]

# attempt to connect with key and 
# if not, add the public key to the remote computer
username = 
keyhandling.writeauthorize(pubkeypath, computer, username, password)

#example command line ref
import paramiko
import socket
import getpass
password = getpass.getpass()
username = 'david'
hostname = 'pipi'
port = 22
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((hostname, port))
t = paramiko.Transport(sock)
t.connect()
t.auth_password(username, password)
sftp_client = paramiko.SFTPClient.from_transport(t)
# do stuff
sftp_client.close()    
t.close()
