import os
import argparse

def filter_and_write_pcap(input_pcap_name, output_pcap_name):
    cmd = 'tcpdump -nr {} -w {} "ip and (tcp or udp)"'.format(input_pcap_name, output_pcap_name)
    os.system(cmd)

def count_and_write_pcap(output_pcap_name, output_metadata_name):
    cmd = "tcpdump -nr {} 2>/dev/null | wc -l | awk '{{$1=$1}};1' > {}".format(output_pcap_name, output_metadata_name)
    os.system(cmd)

def main(args):
    output_pcap_name = args.input_pcap.replace('.pcap', '.tcp_or_udp.pcap')
    output_metadata_name = output_pcap_name.replace('.pcap', '.meta')

    filter_and_write_pcap(args.input_pcap, output_pcap_name)
    count_and_write_pcap(output_pcap_name, output_metadata_name)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_pcap', required=True)
    args = parser.parse_args()
    main(args)
