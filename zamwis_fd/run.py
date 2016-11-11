import os
import sys
import datetime
import logging
import click

fddir = os.path.join(
        os.path.expanduser('~'), 'Documents', 'GitHub',
        'F_and_D_Toolbox', 'scripts', 'F_and_D_Toolbox')
sys.path.append(fddir)
from . import workflow

logging.basicConfig(format='%(module)s - %(message)s', level=logging.INFO)

@click.command()
@click.argument('outdir', type=click.Path(exists=True))
@click.option('--extent', default='18.3,36.6,-20.5,-8.9', help='Extent of interest (xmin,xmax,ymin,ymax) (default: \'18.3,36.6,-20.5,-8.9\')')
@click.option('--startdate', help='Start date YYYYMMDD')
@click.option('--enddate', help='End date YYYYMMDD')
@click.option('--split/--nosplit', default=True, help='Split output files into yearly chunks (default: True)')
def main(outdir, extent,
        startdate=None, enddate=None,
        split=True):

    if enddate is None:
        enddate = datetime.datetime.now()
        enddate_str = enddate.strftime('%Y%m%d')

    if startdate is None:
        startdate = enddate - datetime.timedelta(days=10)
        startdate_str = startdate.strftime('%Y%m%d')

    workflow.update_products(outdir=outdir, extent=extent,
            startdate=startdate_str, enddate=enddate_str, split=split)

if __name__ == '__main__':

    main()