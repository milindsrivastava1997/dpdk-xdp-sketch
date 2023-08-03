import os
import sys
import argparse

pcap_dir = "/scratch/"
pcaps = [
    "equinix-nyc.dirA.20180517-130900.UTC.anon.tcp_or_udp.rewrite.pcap",
    "equinix-nyc.dirA.20180517-131000.UTC.anon.tcp_or_udp.rewrite.pcap",
    "equinix-nyc.dirA.20180517-131100.UTC.anon.tcp_or_udp.rewrite.pcap"
]

# DPDK
#sketches = ['CM', 'Count', 'UnivMon']
# XDP
sketches = ['CM', 'Count']

params = {}
params['CM'] = [(3, 65536, 1)]
params['Count'] = [(3, 65536, 1)]
params['UnivMon'] = [(3, 65536, 6)]

def main(args):
    exp_dir = os.path.join(os.path.expanduser('~milindsr'), args.exp_name)
    os.makedirs(exp_dir, exist_ok=True)

    for sketch in sketches:
        for pcap in pcaps:
            for param in params[sketch]:
                out_dir = os.path.join(exp_dir, args.dataplane, sketch, pcap)
                os.makedirs(out_dir, exist_ok=True)
                cmd = 'sudo python3 execute_receiver.py --output_dir {} --dataplane {} --sketch {} --pcap {} --rows {} --width {} --levels {} --comm_port {}'
                cmd = cmd.format(out_dir, args.dataplane, sketch, os.path.join(pcap_dir, pcap), param[0], param[1], param[2], args.comm_port)
                os.system(cmd)
                args.comm_port += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataplane', required=True)
    parser.add_argument('--exp_name', required=True)
    parser.add_argument('--comm_port', default=4000, type=int)
    args = parser.parse_args()
    main(args)
