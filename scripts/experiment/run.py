import os
import sys
import argparse

def get_param_range(row_range, col_range, level_range):
    return [(row, 2**col, level) for row in row_range for col in col_range for level in level_range]

pcap_dir = "/scratch/caida/"
pcaps = [
    "equinix-nyc.dirA.20180517-130900.UTC.anon.tcp_or_udp.rewrite.pcap",
    "equinix-nyc.dirA.20180517-131000.UTC.anon.tcp_or_udp.rewrite.pcap",
    "equinix-nyc.dirA.20180517-131100.UTC.anon.tcp_or_udp.rewrite.pcap",
    "equinix-nyc.dirA.20180621-130900.UTC.anon.tcp_or_udp.rewrite.pcap",
    "equinix-nyc.dirA.20180621-131000.UTC.anon.tcp_or_udp.rewrite.pcap",
    "equinix-nyc.dirA.20180621-131100.UTC.anon.tcp_or_udp.rewrite.pcap",
    "equinix-nyc.dirA.20180816-130900.UTC.anon.tcp_or_udp.rewrite.pcap",
    "equinix-nyc.dirA.20180816-131000.UTC.anon.tcp_or_udp.rewrite.pcap",
    "equinix-nyc.dirA.20180816-131100.UTC.anon.tcp_or_udp.rewrite.pcap",
    "equinix-nyc.dirA.20181018-130900.UTC.anon.tcp_or_udp.rewrite.pcap",
    "equinix-nyc.dirA.20181018-131000.UTC.anon.tcp_or_udp.rewrite.pcap",
    "equinix-nyc.dirA.20181018-131100.UTC.anon.tcp_or_udp.rewrite.pcap",
    "equinix-nyc.dirA.20181115-130900.UTC.anon.tcp_or_udp.rewrite.pcap",
    "equinix-nyc.dirA.20181115-131000.UTC.anon.tcp_or_udp.rewrite.pcap",
    "equinix-nyc.dirA.20181115-131100.UTC.anon.tcp_or_udp.rewrite.pcap",
    "equinix-nyc.dirA.20181220-130900.UTC.anon.tcp_or_udp.rewrite.pcap",
    "equinix-nyc.dirA.20181220-131000.UTC.anon.tcp_or_udp.rewrite.pcap",
    "equinix-nyc.dirA.20181220-131100.UTC.anon.tcp_or_udp.rewrite.pcap"
]

# DPDK
sketches = ['CM', 'Count', 'UnivMon']
# XDP
#sketches = ['CM', 'Count']

params = {}
params['CM'] = get_param_range(range(1, 6), range(12, 18), range(1, 2))
params['Count'] = get_param_range(range(1, 6), range(12, 18), range(1, 2))
params['UnivMon'] = get_param_range(range(3, 6), range(8, 14), range(16, 17))

def main(args):
    exp_dir = os.path.join(os.path.expanduser('~milindsr'), args.exp_name)
    os.makedirs(exp_dir, exist_ok=True)

    for sketch in sketches:
        for pcap in pcaps:
            for param in params[sketch]:
                param_dir_name = 'row_{}_width_{}_level_{}'.format(param[0], param[1], param[2])
                out_dir = os.path.join(exp_dir, args.dataplane, sketch, pcap, param_dir_name)
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
