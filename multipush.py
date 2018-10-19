#!/usr/bin/env python3

import os
import getpass
import socket
import shutil

import appdirs
import yaml

import keyhandling


homedir = os.path.expanduser("~")
user_config = appdirs.user_config_dir()
username = getpass.getuser()
hostname = socket.gethostname()
comment = "multipush-" + username + "@" + hostname

user_app_dir = os.path.join(user_config, "multipush")
computerfile = os.path.join(user_app_dir, "computers.yml")
key_dir = os.path.join(user_app_dir, "keys")
prvkeypath = os.path.join(key_dir, "id_rsa")
pubkeypath = os.path.join(key_dir, "id_rsa.pub")
# check if private and public keys are present on local client
# filepaths are .config/multipush/keys/keyname

def local_keys():
    if not os.path.exists(user_app_dir):
        os.makedirs(user_app_dir)
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

def get_computerlists():
    if not os.path.exists(user_app_dir):
        os.makedirs(user_app_dir)
    if not os.path.exists(computerfile):
        # for now just copy a config file over
        # later can trigger 'New List' dialog
        shutil.copyfile('computers.yml', computerfile)
    with open(computerfile, 'r') as stream:
        computerlists = yaml.safe_load(stream)
    
    return computerlists 

def write_computerlists(computerlists):
    with open(computerfile, 'w') as stream:
        yaml.dump(computerlists, stream)

def add_public_key(username, password, computers):
    for computer in computers:
        print('authorise public key for ' + username + '@' + computer)
        #keyhandling.writeauthorize(pubkeypath, computer, username, password)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(computername, username=username, password=password, key_filename=prvkeypath)

def check_computer_status(computer):
    # for connection
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        result = sock.connect_ex((computer, 22))
    except socket.gaierror:
        # unable to resolve host name
        result = 999


    # 111 is online but ssh port (22) is not open    
    if result == 999:
        status = 'unresolved'

    if result == 111:
        status = 'closed'

    # 113 not online
    elif result == 113:
        status = 'offline'

    # 0 is avalable and ssh port (default 22) is open   
    elif result == 0:
        status = 'open'

    return status

'''
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
'''
