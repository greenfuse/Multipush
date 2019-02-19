#!/usr/bin/env python3

import socket
import paramiko

sshdir = ".ssh"

def makenewkeys(prvkeypath, pubkeypath, comment):
    newkey = paramiko.RSAKey.generate(bits=4096)
    newkey.write_private_key_file(prvkeypath)
    pubkey = newkey.get_base64()
    pubname = newkey.get_name()
    with open(pubkeypath, "w") as f:
        f.write("%s %s %s" % (pubname, pubkey, comment))

def makepubkey(prvkeypath, pubkeypath, comment):
    privkey = paramiko.rsakey.RSAKey(filename=prvkeypath)
    pubkey = privkey.get_base64()
    pubname = newkey.get_name()
    with open(pubkeypath, "w") as f:
        f.write("%s %s %s" % (pubname, pubkey, comment))

def writeauthorise (keyfile, computer, port, username, password):
    '''
    create the .ssh directory if necessary and append to or create the
    authorized_keys file with the public key
    '''
    f = open(keyfile, "r")
    key = f.read()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((computer, port))
    t = paramiko.Transport(sock)
    t.connect()
    t.auth_password(username, password)
    # note - use the above with t.auth_publickey for key authentication
    sftp_client = paramiko.SFTPClient.from_transport(t)
                    
    # Paramiko sftp can do append/create and chmod
    # need to check for and create if necessary the ~/.ssh directory
    if not sshdir in sftp_client.listdir(path = "."):
        sftp_client.mkdir(sshdir, mode=0o700)
        
    with sftp_client.open(".ssh/authorized_keys", "a") as f:
        f.write(key)
    sftp_client.chmod(".ssh/authorized_keys", 0o600)
    # exit sftp and ssh clients
    sftp_client.close()
    t.close()
