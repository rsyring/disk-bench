from diskbench import fio
from diskbench.testing import load_json


def test_fio(tmpdir):
    stats = fio.fio(tmpdir.strpath, seq_size='1m', rand_size='512k')

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
