__author__ = 'lex'
import argparse

import numpy as np
import matplotlib.pyplot as plt
from fastnumbers import isfloat


def get_file_key(inFile):
    name = inFile.name.split('/')[-1]
    if 'redisSS' in name:
        return 'redisSS'
    return 'redis'


def extract_data(inputFiles, labels):
    data = {}

    for label in labels:
        if label not in data.keys():
            data[label] = {}

        for inFile in inputFiles:
            fname = get_file_key(inFile)
            data[label][fname] = []
            key = '['+label.upper()+']'
            for line in inFile:
                if line.startswith(key):
                    line = line.rstrip('\n')
                    line = line.split(',')
                    if len(line) == 3 and isfloat(line[1]):
                        data[label][fname].append(float(line[2]))
    return data

def get_cdf_data(data, labels):


    maxNonZero=0
    for label in labels:
        for key in data[label].keys():
            data[label][key] = np.array(data[label][key])
            nonZeroMax = np.amax(np.nonzero(data[label][key]))
            if nonZeroMax > maxNonZero:
                maxNonZero = nonZeroMax
            data[label][key] /= data[label][key].sum()
            data[label][key] = np.cumsum(data[label][key])

            if data[label][key][0] > 0.:
                data[label][key] = np.insert(data[label][key], 0, 0.)

    for label in labels:
        for key in data[label]:
            data[label][key] = data[label][key][:maxNonZero]



    return data

def plot_cdf(data, labels, outputFile, fieldSize):

    colors = {'redis':'r', 'redisSS':'b'}
    markers={'redis':'>', 'redisSS':'o'}
    line_style = {'redis':'.', 'redisSS':'--'}
    for l in labels:
        for k in data[l].keys():
            plt.plot(data[l][k], colors[k],
                    label=k,
                    linewidth=2,
                    marker=markers[k],
                    markersize=12)


    plt.grid(True)
    plt.title("field size "+fieldSize +" bytes")
    plt.ylim(0,1.05)
    plt.ylabel("CDF")
    plt.xlabel("ms")
    plt.legend(loc=4)


    plt.savefig(outputFile)


def main():

    parser = argparse.ArgumentParser(description="CDF generation script")
    parser.add_argument('-i',
                        '--input',
                        type=file,
                        nargs='+',
                        help='Input files to read CDF data from',
                        required=True)

    parser.add_argument('-l',
                        '--labels',
                        type=str,
                        nargs='+',
                        help='Labels to look inside the data files',
                        required=True)

    parser.add_argument('-o',
                        '--output',
                        type=str,
                        help='Output file prefix',
                        required=True)

    parser.add_argument('-b',
                        '--bins',
                        type=int,
                        help='Number of bins',
                        default=1000)

    parser.add_argument('-f',
                        '--field',
                        type=str,
                        help='Field Size',
                        required=True)

    args = parser.parse_args()
    data = extract_data(args.input, args.labels)
    data = get_cdf_data(data, args.labels)
    plot_cdf(data, args.labels, args.output, args.field)

if __name__ == "__main__":
    main()