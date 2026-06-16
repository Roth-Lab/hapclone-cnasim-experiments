import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from utils import plot_results

def main(args):

    in_paths = [args.ploidy_file, args.hamming_file, args.max_file, args.min_file, args.between_file, args.within_file]
    out_paths_scatter = [args.ploidy_scatter, args.hamming_scatter, args.max_scatter, args.min_scatter, args.between_scatter, args.within_scatter]
    out_paths_error = [args.ploidy_error, args.hamming_error, args.max_error, args.min_error, args.between_error, args.within_error]
    titles = ['Average ploidy error', 
            'Average hamming distance', 
            'Average maximum distance between cells in a clone', 
            'Average minimum distance between cell in a clone and cell not in a clone', 
            'Average distance from all cells in a clone to cells not in the clone', 
            'Average distance between all cells within a clone']
    colours=['palevioletred', 'thistle', 'cornflowerblue', 'lightskyblue', 'limegreen', 'moccasin', 'orangered']

    for i in range(len(titles)):
        in_path=in_paths[i]
        labels, results, methods = _get_data_(in_path)
        error_plot=_plot_errorbars_(results, methods, titles[i], colours)
        error_plot.savefig(out_paths_error[i])
        plt.clf()
        scatter_plot=_plot_scatter_(results, methods, labels, titles[i], colours)
        scatter_plot.savefig(out_paths_scatter[i])
        plt.clf()

def _get_data_(paths):
    results = []
    labels = []
    for i in range(len(paths)):
        path = paths[i]
        df = pd.read_csv(path, sep='\t', index_col='Unnamed: 0')
        results.append(df.mean().values)
        labels.append(str(path).split("/")[-4])
    results = np.array(results)
    methods = df.columns.values
    return labels, results, methods

def _plot_errorbars_(data, cols, title, colours):
    x = np.arange(data.shape[1])
    y = data.mean(axis=0)
    mins = data.min(axis=0)
    maxs = data.max(axis=0)

    fig, ax = plt.subplots(figsize=(10, 10))
    for i in range(len(x)):
        ax.errorbar(x[i], y[i], fmt='o', 
                    yerr=np.array((y[i] - mins[i], maxs[i] - y[i])).reshape(2, 1),
                    mfc=colours[i], 
                    mec=colours[i], 
                    ecolor=colours[i])
    ax.set_xticks(x, labels=cols, rotation=90, fontsize=6)
    #ax.set_ylim(0, 2)
    ax.set_title(title)
    return plt

def _plot_scatter_(data, cols, labels, title, colours):
    fig, ax = plt.subplots(figsize=(8, 8))
    x = np.arange(1, data.shape[0] + 1)
    for i in range(data.shape[1]):
        ax.scatter(x, data[:, i], s=10, alpha=0.5, c=colours[i])
    #ax.set_ylim(0, 2)
    ax.set_title(title)
    ax.legend(cols, ncol=2, fontsize=8)
    ax.set_xticks(x, labels = labels, rotation=90, fontsize=8)
    return plt

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("-p", "--ploidy-file", nargs="+", required=True)

    parser.add_argument("-ps", "--ploidy-scatter", required=True)

    parser.add_argument("-pe", "--ploidy-error",  required=True)

    parser.add_argument("-ha", "--hamming-file", nargs="+", required=True)

    parser.add_argument("-hs", "--hamming-scatter",  required=True)

    parser.add_argument("-he", "--hamming-error", required=True)

    parser.add_argument("-ma", "--max-file", nargs="+", required=True)

    parser.add_argument("-mas", "--max-scatter", required=True)

    parser.add_argument("-mae", "--max-error", required=True)

    parser.add_argument("-mi", "--min-file", nargs="+", required=True)

    parser.add_argument("-mis", "--min-scatter", required=True)

    parser.add_argument("-mie", "--min-error", required=True)

    parser.add_argument("-b", "--between-file", nargs="+", required=True)

    parser.add_argument("-bs", "--between-scatter", required=True)

    parser.add_argument("-be", "--between-error", required=True)

    parser.add_argument("-w", "--within-file", nargs="+", required=True)

    parser.add_argument("-ws", "--within-scatter", required=True)

    parser.add_argument("-we", "--within-error", required=True)

    cli_args = parser.parse_args()

    main(cli_args)