#!/usr/bin/env python3

import os
import getpass
import socket
import shutil
import sys
import time
import select

import appdirs
import yaml
import paramiko

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
prvkey = paramiko.RSAKey(filename=prvkeypath)


# check if private and public keys are present on local client
# filepaths are .config/multipush/keys/keyname

def local_keys():
    if not os.path.exists(user_app_dir):
        os.makedirs(user_app_dir)
    if not os.path.exists(key_dir):
        os.makedirs(key_dir)
        os.chmod(user_app_dir, 0o700)
        os.chmod(key_dir, 0o700)
        keyhandling.makenewkeys(prvkeypath, pubkeypath, comment)
    elif not os.path.exists(prvkeypath):
        keyhandling.makenewkeys(prvkeypath, pubkeypath, comment)
    elif not os.path.exists(pubkeypath):
        keyhandling.makepubkey(prvkeypath, pubkeypath, comment)

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
        keyhandling.writeauthorise(pubkeypath, computer, 22, username, password)
        #ssh = paramiko.SSHClient()
        #ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #ssh.connect(computername, port=22, username=username, password=password, key_filename=pubkeypath)

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

def run_command(computer, username, command):
    print("run " + command + "on " + computer)

    i = 1
    # Retry a few times if it fails.
    #
    while True:
        print("Trying to connect to %s (%i/5)" % (computer, i))

        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(computer, username=username, pkey=prvkey)
            print("Connected to %s" % computer)
            break
        except paramiko.AuthenticationException:
            print( "Authentication failed when connecting to %s" % computer)
            return
        except:
            print( "Could not SSH to %s, waiting for it to start" % computer)
            i += 1
            time.sleep(2)

        # If we could not connect within time limit
        if i == 5:
            print("Could not connect to %s. Giving up" % computer)
            return

        # Send the command (non-blocking)
        stdin, stdout, stderr = ssh.exec_command(command)
        result = (stdin, stdout, stderr)

        #
        # Disconnect from the host
        #
        print("Command done, closing SSH connection")
        ssh.close()
        return result








def copy_file(computer, source, destination):
    print("copy file to " + computer)



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
