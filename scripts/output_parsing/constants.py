PCAPS = ['equinix-nyc.dirA.20180517-130900.UTC.anon.tcp_or_udp.rewrite.pcap', 'equinix-nyc.dirA.20180517-131100.UTC.anon.tcp_or_udp.rewrite.pcap', 'equinix-nyc.dirA.20180517-131000.UTC.anon.tcp_or_udp.rewrite.pcap']

DP_SKETCH_MAP = {
    'dpdk': ['CM', 'Count', 'UnivMon'],
    'xdp': ['CM', 'Count']
}
SKETCH_NAME_MAP = {
    'CM': 'cm',
    'Count': 'cs',
    'UnivMon': 'univmon'
}

FLOWKEY = 'dstIP,dstPort'
