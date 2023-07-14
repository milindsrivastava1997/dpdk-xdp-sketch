import os
import time
import pickle
import psutil
import signal
import socket
import argparse
import subprocess

import utils
import constants

def start_receiver(args):
    sketch_dir = os.path.join(constants.ROOT_DIR_MAP[args.dataplane], args.sketch)
    sketch_out = os.path.join(args.output_dir, 'sketch_out')
    # compile
    #compile_cmd = '(cd {}; {})'.format(sketch_dir, constants.COMPILE_CMD_MAP[args.dataplane])
    compile_cmd = constants.COMPILE_CMD_MAP[args.dataplane]
    utils.execute_in_shell(compile_cmd, cwd=sketch_dir)
    # run
    run_cmd = constants.RUN_CMD_MAP[args.dataplane].format(args.num_packets, sketch_out)
    return utils.execute_with_popen(run_cmd, cwd=sketch_dir)

def get_dst_mac():
    output = subprocess.check_output("ip a | grep 'inet 10.10.1.1/24' -B1 | head -n1 | awk '{print $2}'", shell=True)
    return output.decode('utf-8').strip()

def start_sender_helper(args):
    sender_helper_dir = os.path.join(constants.ROOT_DIR, 'scripts', 'experiment')
    sender_helper_out = os.path.join(args.output_dir, 'sender_helper_out')

    run_cmd = 'python3 -u sender_helper.py --comm_port {} --pcap {} --num_packets {} --dstmac {} --output_dir {} > {} 2>&1 &'
    run_cmd = run_cmd.format(args.comm_port, args.pcap, args.num_packets, get_dst_mac(), args.output_dir, sender_helper_out)
    
    final_run_cmd = '(cd {}; mkdir -p {}; {})'.format(sender_helper_dir, args.output_dir, run_cmd)
    #utils.execute_in_shell(run_cmd, cwd=sender_helper_dir)
    ssh_cmd = utils.get_ssh_cmd(constants.SENDER_USERNAME, constants.SENDER_IP, final_run_cmd, sudo=True)
    utils.execute_in_shell(ssh_cmd)
    time.sleep(5)

def kill_receiver_when_done(receiver_popen):
    time.sleep(constants.MAX_RECEIVER_WAIT)
    pids = []
    pid = receiver_popen.pid
    process = psutil.Process(pid)
    children = process.children(recursive=True)
    for c in children:
        os.kill(c.pid, signal.SIGINT)

def setup_socket(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket created')
    sock.bind((constants.RECEIVER_IP, port))
    print('Socket bound')
    sock.connect((constants.SENDER_IP, port))
    print('Socket connected')
    return sock

def main(args):
    os.makedirs(args.output_dir, exist_ok=True)
    # run receiver
    receiver_popen = start_receiver(args)
    # execute sender_helper with --pcap --num_packets --dstmac
    start_sender_helper(args)
    # initialize socket
    sock = setup_socket(args.comm_port)
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
    parser.add_argument('--num_packets', type=int, required=True)

    args = parser.parse_args()
    main(args)
