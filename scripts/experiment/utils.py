import time
import shlex
import select
import struct
import subprocess

import constants

def get_ssh_cmd(username, ip, cmd, sudo=False):
    ssh_cmd = 'ssh {} {}@{} "{}"'.format(constants.SSH_FLAGS, username, ip, cmd)
    if sudo:
        ssh_cmd = 'sudo ' + ssh_cmd
    return ssh_cmd

def execute_in_shell(cmd, cwd=None):
    print(cmd)
    return subprocess.run(cmd, shell=True, cwd=cwd)

def execute_with_popen(cmd, cwd=None):
    print(cmd)
    popen = subprocess.Popen(cmd, cwd=cwd, shell=True)
    return popen

def check_socket(sock):
    idx = 0
    ready_sockets = []
    print('Checking socket')
    while len(ready_sockets) == 0 and idx < constants.NETWORK_RETRIES:
        ready_sockets, _, _ = select.select([sock], [], [], 0)
        print('Socket ready: ', str(len(ready_sockets)))
        idx += 1
        time.sleep(1)

    return len(ready_sockets) > 0

def send_msg(sock, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)

def recv_msg(sock):
    raw_msg_len = recvall(sock, 4)
    if not raw_msg_len:
        assert(False)
    msg_len = struct.unpack('>I', raw_msg_len)[0]
    data = recvall(sock, msg_len)
    if data is None:
        assert(False)
    return data

def recvall(sock, n):
    data = b''

    #if not check_socket(sock):
    #    return None

    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data
