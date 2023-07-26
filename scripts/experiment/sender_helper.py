import os
import sys
import pickle
import socket
import argparse
import threading
import traceback

import utils
import constants

def setup_socket(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket created')
    try:
        sock.bind((constants.SENDER_IP, port))
    except:
        print('Bind failed ', str(sys.exc_info()))
        sys.exit()
    print('Socket bound')
    sock.listen(5)
    print('Socket listening')
    connection, address = sock.accept()
    ip, port = str(address[0]), str(address[1])
    print('Connected with ', ip, port)
    return connection

def start_sender(args, num_packets):
    # copy sender.lua to pktgen directory
    copy_cmd = 'cp {} {}'.format(os.path.join(constants.ROOT_DIR, 'scripts', 'experiment', 'sender.lua'), constants.PKTGEN_INSTALL_DIR)
    # set environment variables in sender for lua script
    export_cmd = 'export MY_COUNT={}; export MY_DSTMAC={}'.format(num_packets, args.dstmac)
    # start pktgen on sender
    pktgen_cmd = constants.PKTGEN_CMD.format(constants.PKTGEN_INSTALL_DIR, constants.SENDER_PCI, constants.SENDER_LUA_SCRIPT, os.path.join(args.output_dir, 'pktgen.log'), args.pcap)
    sender_cmd = '({}; {}; {})'.format(copy_cmd, export_cmd, pktgen_cmd)
    utils.execute_in_shell(sender_cmd, cwd=constants.PKTGEN_SCRIPT_DIR)

def get_num_packets(pcap_name):
    metadata_file_name = pcap_name.replace('.pcap', '.meta')
    if not os.path.exists(metadata_file_name):
        assert(False)
    lines = open(metadata_file_name).readlines()
    return int(lines[0].strip())

def main(args):
    os.makedirs(args.output_dir, exist_ok=True)
    # read pcap metadata file
    num_packets = get_num_packets(args.pcap)
    # setup socket
    sock = setup_socket(args.comm_port)
    # run pktgen sender
    start_sender(args, num_packets)
    # tell receiver that sender is done
    utils.send_msg(sock, pickle.dumps('done'))
    # close socket and exit
    sock.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--comm_port', type=int, required=True)

    parser.add_argument('--pcap', required=True)
    parser.add_argument('--dstmac', required=True)
    parser.add_argument('--output_dir', required=True)

    args = parser.parse_args()
    main(args)

