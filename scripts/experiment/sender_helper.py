import os
import sys
import socket
import argparse
import threading
import traceback

import utils

def setup_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STEAM)
    try:
        sock.bind()
    except:
        print('Bind failed ', str(sys.exc_info()))
        sys.exit()
    sock.listen(5)
    print('Socket listening')
    return sock

#def start_server(sock):
#    while True:
#        connection, address = sock.accept()
#        ip, port = str(address[0]), str(address[1])
#        print('Connected with ', ip, port)
#
#        try:
#            t = threading.Thread(target=thread_main, args=)
#            t.start()
#        except:
#            print('Thread did not start')
#            traceback.print_exc()
#
#    sock.close()

def start_sender(args, num_packets):
    # set environment variables in sender for lua script
    export_cmd = 'export MY_COUNT={}; export MY_DSTMAC={}'.format(num_packets, args.dstmac)
    # start pktgen on sender
    pktgen_cmd = ''
    sender_cmd = '{}; {}'.format(export_cmd, pktgen_cmd)
    utils.execute_in_shell(sender_cmd)

def main(args):
    sock = setup_socket()
    connection, address = sock.accept()
    ip, port = str(address[0]), str(address[1])
    print('Connected with ', ip, port)

    # get number of TCP/UDP packets
    if not args.num_packets:
        # search for pcap metadata file
        metadata_file_name = args.pcap + '.meta'
        # if metadata file not found, count number of packets and write to metadata file
        if not os.path.exists(metadata_file_name):
            num_packets = count_packets(args.pcap)
            with open(metadata_file_name, 'w') as fout:
                fout.write(str(num_packets))
        else:
            num_packets = int(open(metadata_file_name).readlines()[0].strip())
    else:
        num_packets = args.num_packets

    # run pktgen sender
    start_sender(args, num_packets)
    # tell receiver that sender is done
    send_msg(sock, pickle.dumps("done"))
    # close socket and exit
    sock.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--comm_port', type=int, required=True)

    parser.add_argument('--pcap', required=True)
    parser.add_argument('--dstmac', required=True)
    parser.add_argument('--num_packets', type=int)

    args = parser.parse_args()
    main(args)

