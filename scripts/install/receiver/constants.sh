#!/bin/bash
NEW_KERNEL="5.15.0-72-generic"

line_to_add="FORCE_SUBDIR_LIBBPF=1"
file_to_modify="./configure"
