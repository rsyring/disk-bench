import csv
import io
import logging

import click
import tableprint as tp

from diskbench import fio

log = logging.getLogger(__name__)


@click.command()
@click.argument('fpath', type=click.Path(exists=False))
@click.option('--size', default='1G')
@click.option('--loops', default=3)
@click.option('--style', default='table', type=click.Choice(['table', 'csv']))
@click.option('--direct', is_flag=True, default=True)
def db(fpath, size, loops, style, direct):
    stats = fio.fio(fpath, loops, size, direct)
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
    header = ['Job', 'bw (MB/s)', 'iops', 'User CPU', 'System CPU']
    formatted_stats = [format_stat(stat) for stat in stats]

    assert style in ('table', 'csv')
    if style == 'table':
        tp.table(formatted_stats, header, out=out_fo, style='round')
    else:
        writer = csv.writer(out_fo, lineterminator='\n')
        writer.writerow(header)
        writer.writerows(formatted_stats)

    out_fo.seek(0)
    return out_fo.read()
