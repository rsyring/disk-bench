from collections import namedtuple
import os

import json

import sh

JobStat = namedtuple('JobStat', 'name bw iops usr_cpu sys_cpu')


def fio(dpath, loops, size, direct):
    direct_num = '1' if direct else '0'
    result = sh.fio(
        '--directory', dpath,
        '--filename=disk~bench.tmp',
        '--output-format=json',
        '--loops={}'.format(loops),
        '--size={}'.format(size),
        '--stonewall',
        '--ioengine=libaio',
        '--direct={}'.format(direct_num),
        '--name=seqread', '--bs=1m', '--rw=read',
        '--name=seqwrite', '--bs=1m', '--rw=write',
        '--name=randread', '--bs=512k', '--rw=randread',
        '--name=randwrite', '--bs=512k', '--rw=randwrite',
        '--name=4kQD32read', '--bs=4k', '--iodepth=32', '--rw=randread',
        '--name=4kQD32write', '--bs=4k', '--iodepth=32', '--rw=randwrite',
    )

    db_tmp_fpath = os.path.join(dpath, 'disk~bench.tmp')
    if os.path.exists(db_tmp_fpath):
        os.unlink(db_tmp_fpath)

    assert not result.stderr, result.stderr

    fio_data = json.loads(result.stdout.decode('utf-8'))

    return extract_stats(fio_data)


def extract_stats(fio_data):
    return (
        extract_job_stats(fio_data['jobs'][0], 'read'),
        extract_job_stats(fio_data['jobs'][1], 'write'),
        extract_job_stats(fio_data['jobs'][2], 'read'),
        extract_job_stats(fio_data['jobs'][3], 'write'),
        extract_job_stats(fio_data['jobs'][4], 'read'),
        extract_job_stats(fio_data['jobs'][5], 'write'),
    )


def extract_job_stats(job_data, io_key):
    return JobStat(
        job_data['jobname'],
        job_data[io_key]['bw'] / 1024,
        job_data[io_key]['iops'],
        job_data['usr_cpu'],
        job_data['sys_cpu'],
    )
