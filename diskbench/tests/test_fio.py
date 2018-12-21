import mock

from diskbench import fio
from diskbench.testing import load_json


def test_fio(tmpdir):
    stats = fio.fio(tmpdir.strpath, loops=1, size='1m', direct=False)

    job_stats = stats[0]
    assert job_stats.name == 'seqread'
    assert job_stats.bw

    job_stats = stats[1]
    assert job_stats.name == 'seqwrite'
    assert job_stats.bw

    job_stats = stats[2]
    assert job_stats.name == 'randread'
    assert job_stats.bw

    job_stats = stats[3]
    assert job_stats.name == 'randwrite'
    assert job_stats.bw

    job_stats = stats[4]
    assert job_stats.name == '4kQD32read'
    assert job_stats.bw

    job_stats = stats[5]
    assert job_stats.name == '4kQD32write'
    assert job_stats.bw


@mock.patch.object(fio, 'sh')
@mock.patch.object(fio, 'extract_stats')
def test_fio_direct(m_es, m_sh):
    m_sh.fio.return_value.stderr = None
    m_sh.fio.return_value.stdout = b'{}'

    fio.fio('/some/path', loops=1, size='1m', direct=True)
    args, kwargs = m_sh.fio.call_args
    assert args[8] == '--direct=1'

    fio.fio('/some/path', loops=1, size='1m', direct=False)
    args, kwargs = m_sh.fio.call_args
    assert args[8] == '--direct=0'


def test_stats_extract():
    data = load_json('fio-output.json')
    stats = fio.extract_stats(data)

    job_stats = stats[0]
    assert job_stats.name == 'seqread'
    assert job_stats.bw == 520126 / 1024
    assert job_stats.iops == 507.94
    assert job_stats.usr_cpu == 0.17
    assert job_stats.sys_cpu == 3.65

    job_stats = stats[1]
    assert job_stats.name == 'seqwrite'
    assert job_stats.bw == 203113 / 1024
    assert job_stats.iops == 198.35
    assert job_stats.usr_cpu == 0.59
    assert job_stats.sys_cpu == 1.08

    job_stats = stats[2]
    assert job_stats.name == 'randread'
    assert job_stats.bw == 582218 / 1024
    assert job_stats.iops == 1137.15
    assert job_stats.usr_cpu == 1.00
    assert job_stats.sys_cpu == 5.28

    job_stats = stats[3]
    assert job_stats.name == 'randwrite'
    assert job_stats.bw == 202819 / 1024
    assert job_stats.iops == 396.13
    assert job_stats.usr_cpu == 0.86
    assert job_stats.sys_cpu == 1.97

    job_stats = stats[4]
    assert job_stats.name == '4kQD32read'
    assert job_stats.bw == 698817 / 1024
    assert job_stats.iops == 174704.44
    assert job_stats.usr_cpu == 19.43
    assert job_stats.sys_cpu == 80.20

    job_stats = stats[5]
    assert job_stats.name == '4kQD32write'
    assert job_stats.bw == 174399 / 1024
    assert job_stats.iops == 43599.83
    assert job_stats.usr_cpu == 9.13
    assert job_stats.sys_cpu == 47.04
