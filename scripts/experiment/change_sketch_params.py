import os
import argparse
import subprocess

import constants

def replace_line(input_file, number, search_string):
    search_string = '#define ' + search_string
    replace_string = search_string + ' ' + str(number)
    cmd = "sed -i 's/{}.*/{}/' {}".format(search_string, replace_string, input_file)
    print(cmd)
    subprocess.check_output(cmd, shell=True)

def set_params(input_file, rows, width, levels=None):
    replace_line(input_file, rows, 'HASH_NUM')
    replace_line(input_file, width, 'LENGTH')
    if levels:
        replace_line(input_file, levels, 'MAX_LEVEL')

def main(args):
    input_dir = os.path.join(constants.ROOT_DIR_MAP[args.dataplane], args.sketch)
    
    for file_name in constants.PARAM_FILE_MAP[args.dataplane]:
        input_file = os.path.join(input_dir, file_name)
        if args.sketch == 'UnivMon':
            set_params(input_file, args.rows, args.width, args.levels)
        else:   
            set_params(input_file, args.rows, args.width, None)
            
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataplane', required=True)
    parser.add_argument('--sketch', required=True)
    parser.add_argument('--rows', required=True, type=int)
    parser.add_argument('--width', required=True, type=int)
    parser.add_argument('--levels', required=True, type=int)
    args = parser.parse_args()
    main(args)
