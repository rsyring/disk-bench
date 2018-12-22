from collections import namedtuple
import os

import json

import sh

JobStat = namedtuple('JobStat', 'name bw iops usr_cpu sys_cpu')


def fio(dpath, seq_size, rand_size):
    randsz_opt = '--size={}'.format(rand_size)
    seqsz_opt = '--size={}'.format(seq_size)

    result = sh.fio(
        '--directory', dpath,
        '--filename=disk~bench.tmp',
        '--output-format=json',
        '--stonewall',
        '--ioengine=libaio',
        '--gtod_reduce=1',
        '--name=seqread', '--bs=1m', '--rw=read', seqsz_opt,
        '--name=seqwrite', '--bs=1m', '--rw=write', seqsz_opt,
        '--name=randread', '--bs=512k', '--rw=randread', randsz_opt,
        '--name=randwrite', '--bs=512k', '--rw=randwrite', randsz_opt,
        '--name=4kQD32read', '--bs=4k', '--iodepth=32', '--rw=randread', randsz_opt,
        '--name=4kQD32write', '--bs=4k', '--iodepth=32', '--rw=randwrite', randsz_opt,
        '--name=4kQD16', '--bs=4k', '--iodepth=32', '--rw=randrw', '--rwmixread=65', randsz_opt,
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
        extract_job_stats(fio_data['jobs'][2], 'read'),
        extract_job_stats(fio_data['jobs'][4], 'read'),
        extract_job_stats(fio_data['jobs'][6], 'read', True),
        extract_job_stats(fio_data['jobs'][1], 'write'),
        extract_job_stats(fio_data['jobs'][3], 'write'),
        extract_job_stats(fio_data['jobs'][5], 'write'),
        extract_job_stats(fio_data['jobs'][6], 'write', True),
    )


def extract_job_stats(job_data, io_key, io_key_name=False):
    job_name = job_data['jobname']
    if io_key_name:
        job_name += io_key

    return JobStat(
        job_name,
        job_data[io_key]['bw'] / 1024,
        job_data[io_key]['iops'],
        job_data['usr_cpu'],
        job_data['sys_cpu'],
    )
