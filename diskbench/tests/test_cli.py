from click.testing import CliRunner

from diskbench import cli
from diskbench import fio
from diskbench.testing import load_json


def invoke_cli(*args):
    runner = CliRunner()
    result = runner.invoke(cli.db, args, catch_exceptions=False)
    assert result.exit_code == 0
    return result


def test_cli_csv(tmpdir):
    result = invoke_cli(tmpdir.strpath, '--style=csv', '--loops=1', '--size=1M')

    assert 'Job,bw (MB/s),iops,User CPU,System CPU' in result.output


def test_format_stats_csv():
    data = load_json('fio-output.json')
    stats = fio.extract_stats(data)
    output = cli.format_stats(stats, 'csv')
    expected = '''
Job,bw (MB/s),iops,User CPU,System CPU
seqread,507.9,508,0.2%,3.6%
seqwrite,198.4,198,0.6%,1.1%
randread,568.6,"1,137",1.0%,5.3%
randwrite,198.1,396,0.9%,2.0%
4kQD32read,682.4,"174,704",19.4%,80.2%
4kQD32write,170.3,"43,600",9.1%,47.0%
'''.lstrip()
    assert output == expected


def test_format_stats_table():
    data = load_json('fio-output.json')
    stats = fio.extract_stats(data)
    output = cli.format_stats(stats, 'table')
    expected = '''
╭─────────────┬─────────────┬─────────────┬─────────────┬─────────────╮
│     Job     │  bw (MB/s)  │    iops     │  User CPU   │ System CPU  │
├─────────────┼─────────────┼─────────────┼─────────────┼─────────────┤
│     seqread │       507.9 │         508 │        0.2% │        3.6% │
│    seqwrite │       198.4 │         198 │        0.6% │        1.1% │
│    randread │       568.6 │       1,137 │        1.0% │        5.3% │
│   randwrite │       198.1 │         396 │        0.9% │        2.0% │
│  4kQD32read │       682.4 │     174,704 │       19.4% │       80.2% │
│ 4kQD32write │       170.3 │      43,600 │        9.1% │       47.0% │
╰─────────────┴─────────────┴─────────────┴─────────────┴─────────────╯
'''.lstrip()
    assert output == expected
