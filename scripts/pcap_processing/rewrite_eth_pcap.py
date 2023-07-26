import os
import shutil
import argparse

def rewrite_pcap(args, output_pcap_name):
    cmd = 'tcprewrite --dlt=enet --enet-smac={} --enet-dmac={} --infile={} --outfile={}'.format(args.src_mac, args.dst_mac, args.input_pcap, output_pcap_name)
    os.system(cmd)

def copy_metadata(input_meta_name, output_meta_name):
    shutil.copy(input_meta_name, output_meta_name)

def main(args):
    output_pcap_name = args.input_pcap.replace('.tcp_or_udp', '.tcp_or_udp.rewrite')
    input_meta_name = args.input_pcap.replace('.pcap', '.meta')
    output_meta_name = output_pcap_name.replace('.pcap', '.meta')

    rewrite_pcap(args, output_pcap_name)
    copy_metadata(input_meta_name, output_meta_name)    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_pcap', required=True)
    parser.add_argument('--src_mac', required=True)
    parser.add_argument('--dst_mac', required=True)
    args = parser.parse_args()
    main(args)
