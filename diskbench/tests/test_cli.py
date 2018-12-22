from click.testing import CliRunner

from diskbench import cli
from diskbench import fio
from diskbench import testing


def invoke_cli(*args):
    runner = CliRunner()
    result = runner.invoke(cli.db, args, catch_exceptions=False)
    assert result.exit_code == 0, result.output
    return result


def test_cli_csv(tmpdir):
    result = invoke_cli(tmpdir.strpath, '--style=csv', '--rand-size=512k', '--seq-size=1m')

    assert 'Stats (MB/s),seqread,randread' in result.output


def test_format_stats_csv():
    data = testing.load_json('fio-output.json')
    stats = fio.extract_stats(data)
    output = cli.format_stats(stats, 'csv')
    expected = '''
Stats (MB/s),seqread,randread,4kQD32read,4kQD16read,seqwrite,randwrite,4kQD32write,4kQD16write
,722.1,209.3,163.0,118.5,"2,909.1","2,709.0","1,321.3",63.7
'''.lstrip()
    assert output == expected


def test_format_stats_table():
    data = testing.load_json('fio-output.json')
    stats = fio.extract_stats(data)
    output = cli.format_stats(stats, 'table')
    # Read from file to avoid flake8 errors b/c table is pretty wide
    expected = testing.read('table-output.txt')
    assert output == expected
