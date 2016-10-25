import os

from flooddrought.ingestion import download_ndvi
from flooddrought.ingestion import download_swi
from flooddrought.ingestion import download_trmm

from flooddrought.indices import update_stats
from flooddrought.indices import calc_ndvi
from flooddrought.indices import calc_swi

from flooddrought.indices import save_spi_stats
from flooddrought.indices import calc_rain

from flooddrought.tools import logs as fdlogs
fdlogs.set_cli_logger()


def update_products(outdir, startdate='', enddate='', extent=''):

    commonkw = dict(
            startdate=startdate, enddate=enddate, extent=extent,
            split_yearly=True)

    outfiles = {}
    for product in ['NDVI', 'SWI', 'TRMM']:
        product_outdir = os.path.join(outdir, product)
        try:
            os.mkdir(product_outdir)
        except OSError:
            pass
        outfiles[product] = os.path.join(product_outdir, (product.lower() + '.nc'))

    # downloads
    download_ndvi.download(outfiles['NDVI'], product_ID=0, **commonkw)
    download_swi.download(outfiles['SWI'], product='SWI', **commonkw)
    download_trmm.download(outfiles['TRMM'], **commonkw)

    # update long-term stats
    for product in ['NDVI', 'SWI']:
        update_stats.update(outfiles[product])

    # update indices
    calc_ndvi.calculate(outfiles['NDVI'], extend_mean=1)
    calc_swi.calculate(outfiles['SWI'], extend_mean=1)

    # update SPI stats
    spi_stats_dir = os.path.join(os.path.dirname(outfiles['TRMM']), 'spi_stats')
    if not os.path.isdir(spi_stats_dir):
        save_spi_stats.save(outfiles['TRMM'], spi_stats_dir=spi_stats_dir)

    # update SPI
    calc_rain.calculate(
            outfiles['TRMM'],
            spi_stats_dir=spi_stats_dir,
            load_into_memory=True)
