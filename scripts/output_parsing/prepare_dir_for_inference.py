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

def compare_params(params_from_dir, params_from_file):
    # dir params
    tokens = params_from_dir.split('_')
    rows = int(tokens[1])
    width = int(tokens[3])
    levels = int(tokens[5])
    if rows == params_from_file['rows'] and width == params_from_file['width'] and levels == params_from_file['levels']:
        return True
    return False

def get_output_dir_name(args, sketch, pcap, level, params):
    output_dir = os.path.join(args.output_root_dir, args.project_name, constants.SKETCH_NAME_MAP[sketch], pcap, constants.FLOWKEY)
    params_dir = 'row_{}_width_{}_level_{}_epoch_60_count_1_seed_1'.format(params['rows'], params['width'], params['levels'])
    output_dir = os.path.join(output_dir, params_dir, '01')
    output_dir = os.path.join(output_dir, 'level_{:02d}'.format(level))
    return output_dir

def dump_files(input_dir, output_dir, params, level):
    # dump counters
    src_path = os.path.join(input_dir, 'parsed_sketch_out.counters_' + str(level))
    dst_path = os.path.join(output_dir, 'sketch_counter.txt')
    shutil.copyfile(src_path, dst_path)
    # dump total.txt
    if params['levels'] > 1:
        with open(os.path.join(output_dir, 'total.txt'), 'w') as fout:
            fout.write('{}\n'.format(params['count_' + str(level)]))
    else:
        assert(level == 0)
        with open(os.path.join(output_dir, 'total.txt'), 'w') as fout:
            fout.write('{}\n'.format(params['total_count']))
    
def main(args):
    input_root_dir = os.path.join(args.input_root_dir, args.dataplane)

    sketches = os.listdir(input_root_dir)

    for sketch in sketches:
        sketch_dir = os.path.join(input_root_dir, sketch)
        pcaps = os.listdir(sketch_dir)
        clean_pcaps = [clean_pcap_name(p) for p in pcaps]

        for pcap, clean_pcap in zip(pcaps, clean_pcaps):
            pcap_dir = os.path.join(sketch_dir, pcap)
            params = os.listdir(pcap_dir)

            for param in params:
                param_dir = os.path.join(pcap_dir, param)
                input_dir = param_dir
                input_file = os.path.join(input_dir, 'sketch_out')
                temp_output_file = os.path.join(input_dir, 'parsed_sketch_out')

                # run parse script
                run_parse_counters(input_file, temp_output_file, args.dataplane)
                # read parsed params
                params_from_file = read_params(temp_output_file + '.params')
                # verify parsed params
                if not compare_params(param, params_from_file):
                    print('Params compare failed!')
                    print(sketch, pcap, param)
                    continue

                for level in range(params_from_file['levels']):
                    # create directory for inference
                    output_dir = get_output_dir_name(args, sketch, clean_pcap, level, params_from_file)
                    os.makedirs(output_dir, exist_ok=True)
                    # copy files for inference
                    dump_files(input_dir, output_dir, params_from_file, level)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_root_dir', required=True)
    parser.add_argument('--output_root_dir', required=True)
    parser.add_argument('--dataplane', required=True)
    parser.add_argument('--project_name', default='QuerySketch')
    args = parser.parse_args()
    main(args)
