import os
import time
import socket
import argparse

import utils
import constants

def start_receiver(args, num_packets):
    sketch_dir = os.path.join(constants.ROOT_DIR_MAP[args.dataplane], sketch)
    sketch_out = os.path.join(args.output_dir, 'sketch_out')
    # compile
    compile_cmd = '(cd {}; {})'.format(sketch_dir, constants.COMPILE_CMD_MAP[args.dataplane])
    utils.execute_in_shell(compile_cmd)
    # run
    run_cmd = constants.RUN_CMD_MAP[args.dataplane].format(num_packets, sketch_out)
    final_run_cmd = '(cd {}; {})'.format(sketch_dir, run_cmd)
    return utils.execute_with_popen(final_run_cmd)

def get_dst_mac():
    return subprocess.check_output("ip a | grep 'inet 10.10.1.1/24' -B1 | head -n1 | awk '{print $2}'", shell=True)

def start_sender_helper(args, num_packets):
    sender_helper_dir = os.path.join(constants.ROOT_DIR, 'scripts', 'experiment')
    sender_helper_out = os.path.join(args.output_dir, 'sender_helper_out')

    if args.num_packets:
        run_cmd = 'python3 sender_helper.py --comm_port {} --pcap {} --num_packets {} --dstmac {} > {} 2>&1 &'
        run_cmd = run_cmd.format(args.comm_port, args.pcap, args.num_packets, get_dst_mac(), sender_helper_out)
    else:
        run_cmd = 'python3 sender_helper.py --comm_port {} --pcap {} --dstmac {} > {} 2>&1 &'
        run_cmd = run_cmd.format(args.comm_port, args.pcap, get_dst_mac(), sender_helper_out)
    
    final_run_cmd = '(cd {}; {})'.format(sender_helper_dir, run_cmd)
    utils.execute_in_shell(final_run_cmd)

def kill_receiver_when_done(receiver_popen):
    # wait for some time
    time.sleep(constants.MAX_RECEIVER_WAIT)
    # kill receiver
    receiver_popen.kill()

    output, error = receiver_popen.communicate()
    
    for line in error:
        if constants.RECEIVER_DONE_STR in line:
            return 0

    # if counters weren't finished printing
    return constants.ERR_NO_COUNTERS

def main(args):
    # run receiver
    receiver_popen = start_receiver(args, num_packets)
    #TODO; execute sender_helper with --pcap --num_packets --dstmac
    start_sender_helper(args, num_packets)
    # wait for "done" from sender, till a certain timeout
    if not utils.check_socket(sock):
        print('Socket communication disrupted!')
        print('Exiting')
        return constants.ERR_SOCKET
    print('Socket:', pickle.loads(utils.recv_msg(sock)))
    # kill receiver
    return kill_receiver_when_done(receiver_popen)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--comm_port', type=int, default=4000)
    parser.add_argument('--output_dir', required=True)

    parser.add_argument('--dataplane', required=True)
    parser.add_argument('--sketch', required=True)
    parser.add_argument('--pcap', required=True)
    parser.add_argument('--num_packets', type=int)

    args = parser.parse_args()
    main(args)
