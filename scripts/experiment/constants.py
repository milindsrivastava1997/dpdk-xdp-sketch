import os

# network
RECEIVER_IP = "10.10.2.1"
SENDER_USERNAME = "root"
SENDER_IP = "10.10.2.2"
SENDER_PCI = "41:00.0"
SENDER_LUA_SCRIPT = "sender.lua"
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
ROOT_DIR = os.path.join(os.path.expanduser('~milindsr'), 'dpdk-xdp-sketch')
ROOT_DIR_MAP = {}
ROOT_DIR_MAP[DPDK] = os.path.join(ROOT_DIR, DPDK.upper())
ROOT_DIR_MAP[XDP] = os.path.join(ROOT_DIR, XDP.upper())

COMPILE_CMD_MAP = {}
COMPILE_CMD_MAP[DPDK] = 'make' 
COMPILE_CMD_MAP[XDP] = './compile.sh'

RUN_CMD_MAP = {}
RUN_CMD_MAP[DPDK] = './build/Ours-thd {} > {}'
RUN_CMD_MAP[XDP] = './main {} > {} 2>&1'

PKTGEN_VERSION = '23.03.0'
PKTGEN_SCRIPT_DIR = os.path.join(ROOT_DIR, 'scripts', 'experiment')
PKTGEN_CMD = './run_pktgen.sh {} {} {} {} {}'
PKTGEN_INSTALL_DIR = os.path.join(ROOT_DIR, 'scripts', 'install', 'sender', 'pktgen-' + PKTGEN_VERSION)

RECEIVER_DONE_STR = "Finished printing counters"
MAX_RECEIVER_WAIT = 10
