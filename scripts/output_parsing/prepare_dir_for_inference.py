import os
import shutil
import argparse
import subprocess

import constants

current_dir = os.path.dirname(os.path.realpath(__file__))

def clean_pcap_name(pcap):
    return pcap.replace('tcp_or_udp.rewrite.', '')

def run_parse_counters(input_file, output_file, dataplane):
    cmd = 'python3 ' + os.path.join(current_dir, 'parse_counters.py')
    cmd += ' --input_file ' + input_file
    cmd += ' --output_file ' + output_file
    cmd += ' --dataplane ' + dataplane

    print(cmd)

    subprocess.run(cmd, shell=True)

def read_params(params_file):
    lines = open(params_file).readlines()
    lines = [line.strip().split(': ') for line in lines]
    params = {line[0]:int(line[1]) for line in lines}
    return params

def get_output_dir_name(args, sketch, pcap, level, params):

    output_dir = os.path.join(args.output_root_dir, args.project_name, constants.SKETCH_NAME_MAP[sketch], pcap, constants.FLOWKEY)
    params_dir = 'row_{}_width_{}_level_{}_epoch_60_count_1_seed_1'.format(params['rows'], params['width'], params['levels'])
    output_dir = os.path.join(output_dir, params_dir, '01')
    output_dir = os.path.join(output_dir, 'level_{:02d}'.format(level))
    return output_dir

def dump_files(input_dir, output_dir, params):
    # dump sketch_counter.txt
    src_path = os.path.join(input_dir, 'parsed_sketch_out.counters')
    dst_path = os.path.join(output_dir, 'sketch_counter.txt')
    shutil.copyfile(src_path, dst_path)
    # dump total.txt
    with open(os.path.join(output_dir, 'total.txt'), 'w') as fout:
        fout.write('{}\n'.format(params['total_count']))
    
def main(args):
    sketches = constants.DP_SKETCH_MAP[args.dataplane]
    clean_pcaps = [clean_pcap_name(p) for p in constants.PCAPS]

    for sketch in sketches:
        for pcap, clean_pcap in zip(constants.PCAPS, clean_pcaps):
            input_dir = os.path.join(args.input_root_dir, args.dataplane, sketch, pcap)
            input_file = os.path.join(input_dir, 'sketch_out')
            temp_output_file = os.path.join(input_dir, 'parsed_sketch_out')

            # run parse script
            run_parse_counters(input_file, temp_output_file, args.dataplane)
            # read parsed params
            params = read_params(temp_output_file + '.params')
            for level in range(params['levels']):
                # create directory for inference
                output_dir = get_output_dir_name(args, sketch, clean_pcap, level, params)
                os.makedirs(output_dir, exist_ok=True)
                # copy files for inference
                dump_files(input_dir, output_dir, params)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_root_dir', required=True)
    parser.add_argument('--output_root_dir', required=True)
    parser.add_argument('--dataplane', required=True)
    parser.add_argument('--project_name', default='QuerySketch')
    args = parser.parse_args()
    main(args)
