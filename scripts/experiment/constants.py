import os

# network
SENDER_USERNAME = "root"
SENDER_IP = "10.10.1.2"
SSH_FLAGS = "-o StrictHostKeyChecking=no"
NETWORK_RETRIES = 500

# error codes
ERR_SOCKET = -1
ERR_NO_COUNTERS = -2

# dataplanes
DPDK = 'dpdk'
XDP = 'xdp'
DATAPLANES = [DPDK, XDP]

# root dirs
ROOT_DIR = os.path.join(os.expanduser('~'), 'dpdk-xdp-sketch')
ROOT_DIR_MAP = {}
ROOT_DIR_MAP[DPDK] = os.path.join(ROOT_DIR, DPDK.upper())
ROOT_DIR_MAP[XDP] = os.path.join(ROOT_DIR, XDP.upper())

COMPILE_CMD_MAP = {}
COMPILE_CMD_MAP[DPDK] = 'make' 
COMPILE_CMD_MAP[XDP] = './compile.sh'

RUN_CMD_MAP = {}
RUN_CMD_MAP[DPDK] = 'sudo ./build/Ours-thd {} > {}'
RUN_CMD_MAP[XDP] = 'sudo ./main {} > {}'

RECEIVER_DONE_STR = "Finished printing counters"
