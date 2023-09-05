import os
import sys
import binascii
import crcmod
import xxhash

def calc_hash(flowkey, seed):
    key_byte = b''
    if "srcIP" in flowkey['key']:
        key_byte += flowkey['src_ip'].to_bytes(4, byteorder='little')
    if "srcPort" in flowkey['key']:
        key_byte += flowkey['src_port'].to_bytes(2, byteorder='little')
    if "dstIP" in flowkey['key']:
        key_byte += flowkey['dst_ip'].to_bytes(4, byteorder='little')
    if "dstPort" in flowkey['key']:
        key_byte += flowkey['dst_port'].to_bytes(2, byteorder='little')
    if "proto" in flowkey['key']:
        key_byte += flowkey['proto'].to_bytes(1, byteorder='little')
    
    #key_bytes = b''
    #key_bytes += (flowkey.dst_addr).to_bytes(4, byteorder='big')
    #key_bytes += (flowkey.dst_port).to_bytes(4, byteorder='big')
    
    #return xxhash.xxh32_intdigest(key_byte[::-1], seed=seed)
    return xxhash.xxh32_intdigest(key_byte, seed=seed)

def main():
    flowkey = {
        'src_ip': 12345678,
        'src_port': 9320,
        'dst_ip':  90152391,
        'dst_port': 8331,
        'proto': 0
    }
    flowkey['key'] = 'srcIP,srcPort,dstIP,dstPort'

    for seed in range(3):
        print(seed, calc_hash(flowkey, seed))

if __name__ == '__main__':
    main()
