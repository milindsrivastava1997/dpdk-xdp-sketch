import os

# network
RECEIVER_IP = "10.10.2.1"
RECEIVER_PCI = "41:00.0"
SENDER_USERNAME = "root"
SENDER_IP = "10.10.2.2"
SENDER_PCI = "41:00.0"
SENDER_LUA_SCRIPT = "sender.lua"
SSH_FLAGS = "-o StrictHostKeyChecking=no"
NETWORK_RETRIES = 3600

# error codes
ERR_SOCKET = -1
ERR_NO_COUNTERS = -2

# dataplanes
DPDK = 'dpdk'
XDP = 'xdp'
DATAPLANES = [DPDK, XDP]

# dirs
ROOT_DIR = os.path.join(os.path.expanduser('~milindsr'), 'dpdk-xdp-sketch')
ROOT_DIR_MAP = {}
ROOT_DIR_MAP[DPDK] = os.path.join(ROOT_DIR, DPDK.upper())
ROOT_DIR_MAP[XDP] = os.path.join(ROOT_DIR, XDP.upper())
EXPERIMENT_SCRIPTS_DIR = os.path.join(ROOT_DIR, 'scripts', 'experiment')

# compile commands
COMPILE_CMD_MAP = {}
COMPILE_CMD_MAP[DPDK] = 'make clean; make' 
COMPILE_CMD_MAP[XDP] = './compile.sh'

# run commands
RUN_CMD_MAP = {}
RUN_CMD_MAP[DPDK] = './build/Ours-thd -a {} > {} 2>&1'
RUN_CMD_MAP[XDP] = './main > {} 2>&1'

# pktgen
PKTGEN_VERSION = '23.03.0'
PKTGEN_CMD = './run_pktgen.sh {} {} {} {} {}'
PKTGEN_INSTALL_DIR = os.path.join(ROOT_DIR, 'scripts', 'install', 'sender', 'pktgen-' + PKTGEN_VERSION)

# misc
RECEIVER_DONE_STR = "Finished printing counters"
MAX_RECEIVER_WAIT = 10

# sketch parameter replacement
CHANGE_PARAMS_CMD = 'python3 change_sketch_params.py --dataplane {} --sketch {} --rows {} --width {} --levels {}'
PARAM_FILE_MAP = {}
PARAM_FILE_MAP[DPDK] = ['config.h']
PARAM_FILE_MAP[XDP] = ['Ours-main.c', 'Ours-XDP.c']
