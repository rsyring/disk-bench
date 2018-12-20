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
