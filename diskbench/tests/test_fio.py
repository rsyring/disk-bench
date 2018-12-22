import mock

from diskbench import fio
from diskbench.testing import load_json


def test_fio(tmpdir):
    stats = fio.fio(tmpdir.strpath, seq_size='1m', rand_size='512k', direct=False)

    job_stats = stats[0]
    assert job_stats.name == 'seqread'
    assert job_stats.bw

    job_stats = stats[1]
    assert job_stats.name == 'randread'
    assert job_stats.bw

    job_stats = stats[2]
    assert job_stats.name == '4kQD32read'
    assert job_stats.bw

    job_stats = stats[3]
    assert job_stats.name == '4kQD16read'
    assert job_stats.bw

    job_stats = stats[4]
    assert job_stats.name == 'seqwrite'
    assert job_stats.bw

    job_stats = stats[5]
    assert job_stats.name == 'randwrite'
    assert job_stats.bw

    job_stats = stats[6]
    assert job_stats.name == '4kQD32write'
    assert job_stats.bw

    job_stats = stats[7]
    assert job_stats.name == '4kQD16write'
    assert job_stats.bw


@mock.patch.object(fio, 'sh')
@mock.patch.object(fio, 'extract_stats')
def test_fio_direct(m_es, m_sh):
    m_sh.fio.return_value.stderr = None
    m_sh.fio.return_value.stdout = b'{}'

    fio.fio('/some/path', seq_size='1m', rand_size='512k', direct=True)
    args, kwargs = m_sh.fio.call_args
    assert args[6] == '--direct=1'

    fio.fio('/some/path', seq_size='1m', rand_size='512k', direct=False)
    args, kwargs = m_sh.fio.call_args
    assert args[6] == '--direct=0'


def test_stats_extract():
    data = load_json('fio-output.json')
    stats = fio.extract_stats(data)

    job_stats = stats[0]
    assert job_stats.name == 'seqread'
    assert job_stats.bw == 739475 / 1024

    job_stats = stats[1]
    assert job_stats.name == 'randread'
    assert job_stats.bw == 214345 / 1024

    job_stats = stats[2]
    assert job_stats.name == '4kQD32read'
    assert job_stats.bw == 166864 / 1024

    job_stats = stats[3]
    assert job_stats.name == '4kQD16read'
    assert job_stats.bw == 121329 / 1024

    job_stats = stats[4]
    assert job_stats.name == 'seqwrite'
    assert job_stats.bw == 2978909 / 1024

    job_stats = stats[5]
    assert job_stats.name == 'randwrite'
    assert job_stats.bw == 2774010 / 1024

    job_stats = stats[6]
    assert job_stats.name == '4kQD32write'
    assert job_stats.bw == 1353001 / 1024

    job_stats = stats[7]
    assert job_stats.name == '4kQD16write'
    assert job_stats.bw == 65216 / 1024
