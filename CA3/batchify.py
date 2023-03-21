from ca3 import netParams
from avatk.batchtk.batchify import batchify
import numpy


def get_weight(conn):
    return netParams['connParams'][conn]['weight']

def get_batchlist(weight, function= numpy.linspace, scaling= 10, size = 8):
    return function( weight / scaling, weight * scaling, size )

conns = {"netParams.connParams.{}.weight".format(conn): get_batchlist(get_weight(conn)) for conn in
         netParams.connParams.keys() if 'AMPA' in conn} # or NMDA or GABA

batchify(conns, bin_size= 50, file_label= "batch_csv/run")