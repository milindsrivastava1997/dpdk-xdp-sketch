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
    # change sketch params
    change_sketch_params_cmd = constants.CHANGE_PARAMS_CMD.format(args.dataplane, args.sketch, args.rows, args.width, args.levels)
    completed_process = utils.execute_in_shell(change_sketch_params_cmd, cwd=constants.EXPERIMENT_SCRIPTS_DIR)
    if completed_process.returncode != 0:
        print('Sketch param change return code', completed_process.returncode)
        return None

    # compile
    compile_cmd = constants.COMPILE_CMD_MAP[args.dataplane]
    completed_process = utils.execute_in_shell(compile_cmd, cwd=sketch_dir)
    if completed_process.returncode != 0:
        print('Compilation return code', completed_process.returncode)
        return None
    
    # run
    if args.dataplane == constants.DPDK:
        run_cmd = constants.RUN_CMD_MAP[args.dataplane].format(constants.RECEIVER_PCI, sketch_out)
    elif args.dataplane == constants.XDP:
        run_cmd = constants.RUN_CMD_MAP[args.dataplane].format(sketch_out)
    popen = utils.execute_with_popen(run_cmd, cwd=sketch_dir)
    time.sleep(10)
    return popen

def get_dst_mac():
    output = subprocess.check_output("ip a | grep 'inet 10.10.1.1/24' -B1 | head -n1 | awk '{print $2}'", shell=True)
    return output.decode('utf-8').strip()

def start_sender_helper(args):
    sender_helper_dir = os.path.join(constants.ROOT_DIR, 'scripts', 'experiment')
    sender_helper_out = os.path.join(args.output_dir, 'sender_helper_out')

    run_cmd = 'python3 -u sender_helper.py --comm_port {} --pcap {} --dstmac {} --output_dir {} > {} 2>&1 &'
    run_cmd = run_cmd.format(args.comm_port, args.pcap, get_dst_mac(), args.output_dir, sender_helper_out)
    
    final_run_cmd = '(cd {}; mkdir -p {}; {})'.format(sender_helper_dir, args.output_dir, run_cmd)
    #utils.execute_in_shell(run_cmd, cwd=sender_helper_dir)
    ssh_cmd = utils.get_ssh_cmd(constants.SENDER_USERNAME, constants.SENDER_IP, final_run_cmd, sudo=True)
    utils.execute_in_shell(ssh_cmd)
    time.sleep(5)

def kill_receiver_when_done(receiver_popen):
    pids = []
    pid = receiver_popen.pid
    process = psutil.Process(pid)
    children = process.children(recursive=True)
    for c in children:
        os.kill(c.pid, signal.SIGINT)
        # wait for process to be killed
        # refer https://stackoverflow.com/questions/568271/how-to-check-if-there-exists-a-process-with-a-given-pid-in-python
        while True:
            try:
                os.kill(c.pid, 0)
            except OSError:
                # PID does not exist
                break
            time.sleep(1)

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
    if receiver_popen is None:
        print('Could not run receiver')
        assert(False)
    # execute sender_helper with --pcap --dstmac
    start_sender_helper(args)
    # initialize socket
    sock = setup_socket(args.comm_port)
    # wait for "done" from sender, till a certain timeout
    if not utils.check_socket(sock):
        print('Socket communication disrupted!')
        kill_receiver_when_done(receiver_popen)
        print('Exiting')
        return constants.ERR_SOCKET
    print('Socket:', pickle.loads(utils.recv_msg(sock)))
    # kill receiver
    kill_receiver_when_done(receiver_popen)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--comm_port', type=int, default=4000)
    parser.add_argument('--output_dir', required=True)

    parser.add_argument('--dataplane', required=True)
    parser.add_argument('--sketch', required=True)
    parser.add_argument('--pcap', required=True)

    parser.add_argument('--rows', required=True, type=int)
    parser.add_argument('--width', required=True, type=int)
    parser.add_argument('--levels', required=True, type=int)

    args = parser.parse_args()
    main(args)
