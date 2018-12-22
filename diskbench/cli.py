import csv
import io
import logging

import click
import tableprint as tp

from diskbench import fio

log = logging.getLogger(__name__)


@click.command()
@click.argument('fpath', type=click.Path(exists=False))
@click.option('--seq-size', default='64G')
@click.option('--rand-size', default='4G')
@click.option('--style', default='table', type=click.Choice(['table', 'csv']))
def db(fpath, style, seq_size, rand_size):
    stats = fio.fio(fpath, seq_size, rand_size)
    click.echo(format_stats(stats, style))


def format_stats(stats, style):
    def format_stat(stat):
        return (
            stat.name,
            '{:,.1f}'.format(stat.bw),
            '{:,.0f}'.format(stat.iops),
            '{:,.1f}%'.format(stat.usr_cpu),
            '{:,.1f}%'.format(stat.sys_cpu),
        )

    out_fo = io.StringIO()
    header = ['Stats (MB/s)']
    header += [stat.name for stat in stats]
    table_rows = [[''] + ['{:,.1f}'.format(stat.bw) for stat in stats]]

    assert style in ('table', 'csv')
    if style == 'table':
        tp.table(table_rows, header, out=out_fo, style='round', width=12)
    else:
        writer = csv.writer(out_fo, lineterminator='\n')
        writer.writerow(header)
        writer.writerows(table_rows)

    out_fo.seek(0)
    return out_fo.read()
