import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from Bio import Phylo
import h5py
from utils import *


def main(args):

    cnasim_profile_file = args.cnasim_file
    tree_file = args.tree_file
    hapclone_file = args.hapclone_file

    _, leaves = load_cnasim_tree(tree_file)

    cnasim = pd.read_csv(cnasim_profile_file, sep="\t")
    cnasim["total"] = cnasim["Acount"].astype(int) + cnasim["Bcount"].astype(int)
    cnasim["baf"] = cnasim["Acount"].astype(int) / cnasim["total"]

    ticks, tick_labels = get_ticks(cnasim)

    with h5py.File(hapclone_file, "r") as fh:
        hapclone_baf = fh["baf"][()]
        bins = fh["bins"][()].astype(str)
        cells = fh["cells"][()].astype(str)

    a = hapclone_baf[:, :, :, 0].sum(axis=2)
    b = hapclone_baf[:, :, :, 1].sum(axis=2)
    total = a + b
    baf = a/total
    num_bins = a.shape[1]
    num_cells = a.shape[0]
    hapclone = pd.DataFrame(data=a.flatten(), columns=["acounts"])
    hapclone["cells"] = np.repeat(cells, num_bins)
    hapclone["bcounts"] = hapclone_baf[:, :, :, 1].sum(axis=2).flatten()
    hapclone["total"] = hapclone["acounts"] + hapclone["bcounts"]
    hapclone["baf"] = hapclone["acounts"] / hapclone["total"]
    bins = [x.split(':') for x in bins]
    hapclone['bins'] = bins*50
    hapclone[['chrom', 'beg', 'end']] = hapclone['bins'].astype('str').str.split(', ', expand=True)
    hapclone['chrom'] = [int(x[5:-1]) for x in hapclone.chrom.values]
    hapclone['beg'] = [int(x[1:-1]) for x in hapclone.beg.values]
    hapclone['end'] = [int(x[1:-2]) for x in hapclone.end.values]
    hapclone = hapclone.sort_values(['cells', 'chrom', 'beg'])


    # Cnasim reads
    cnasim_profile = ordered_profiles("CELL", "total", cnasim, leaves)
    cnasim_baf = ordered_profiles("CELL", "baf", cnasim, leaves)
    hapclone_profile = ordered_profiles('cells', 'total', hapclone, leaves)
    hapclone_baf = ordered_profiles('cells', 'baf', hapclone, leaves)
    names = [
        "CNAsim total readcounts",
        "CNAsim baf",
        "Unphased total readcounts",
        "Unphased BAF",
    ]
    profiles = [cnasim_profile, cnasim_baf, hapclone_profile, hapclone_baf]
    cmap = ["OrRd", "GnBu", "OrRd", "GnBu"]

    fig = plot_profiles(profiles, names, ticks, tick_labels, cmap, 0, None, 2)
    fig.savefig(args.out_file)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("-ha", "--hapclone-file", required=True)

    parser.add_argument("-p", "--cnasim-file", required=True)

    parser.add_argument("-t", "--tree-file", required=True)

    parser.add_argument("-o", "--out-file", required=True)

    cli_args = parser.parse_args()

    main(cli_args)
