#!/bin/bash

source constants.sh

get_libxdp_install_dir()
{
    echo $(grep libdir lib/libxdp/libxdp.pc -m1 | cut -d '=' -f2)
}

modify_configure_file()
{
    line_number=$(grep "()" configure -n -m1 | cut -d ':' -f1)
    sed -i $line_number"i "$configure_line $configure_file
}

modify_makefile()
{
    makefile_line="21"
    sed -i $makefile_line"i "$makefile_line $makefile_file
}

cd /local
git clone https://github.com/xdp-project/xdp-tools.git
cd xdp-tools
git submodule update --init
modify_configure_file
./configure
modify_makefile
make
sudo make install
sudo ldconfig
sudo sh -c "ulimit -l unlimited"

# invoke subshell so that cd is done only for the make install
(cd lib/libxdp; sudo make install)
(cd lib/libbpf/src; sudo make install)

# install libbpf .so files
so_install_dir=$(get_libxdp_install_dir)
sudo cp lib/libbpf/src/*.so* $so_install_dir
sudo ldconfig
