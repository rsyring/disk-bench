.. default-role:: code

Disk Bench
##########

Designed to run similar tests as Crystal Disk Mark using fio with user friendly output options.

Tests ran:

* Sequential read/write w/ 1MB block size
* Random read/write w/ 512K block size
* Queue depth 32 random read/write 4K blocks size

Install
=======

::

    # system install
    $ sudo pip3 install disk-bench

    # user install
    $ pip3 install --user disk-bench

Usage
=====

::

    $ disk-bench --help

    # Default runs fio w/ --loops=3 and --size=1G
    $ disk-bench /mnt/disk-to-test/whatever

    # Show CSV output (for easy copy/paste into Excel or Google Sheets)
    $ disk-bench /mnt/disk-to-test/whatever --style=csv

    # Quick
    $ disk-bench /mnt/disk-to-test/whatever --loops=1 --size=1M


Command Details
===============

The `fio` command we are running is essentially:

    fio --directory . --filename=disk~bench.tmp --output-format=json --stonewall \
    --ioengine=libaio --direct=0 --gtod_reduce=1 \
    --name=seqread --bs=1m --rw=read --size=64G \
    --name=seqwrite --bs=1m --rw=write --size=64G \
    --name=randread --bs=512k --rw=randread --size=4G \
    --name=randwrite --bs=512k --rw=randwrite --size=4G \
    --name=4kQD32read --bs=4k --iodepth=32 --rw=randread --size=4G \
    --name=4kQD32write --bs=4k --iodepth=32 --rw=randwrite --size=4G \
    --name=4kQD16 --bs=4k --iodepth=32 --rw=randrw --rwmixread=65 --size=4G
