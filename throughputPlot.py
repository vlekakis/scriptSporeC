__author__ = 'lex'

import argparse
import commands as cmd
import itertools
import matplotlib.pyplot as plt


def proc_data(fileDir):

    label = {
        'load_':'[INSERT]',
        'loadSS_':'[SSS-SIGN-INSERT]',
        'run_read': '[READ]',
        'run_update': '[UPDATE]',
        'runSS_update': '[SSS-SIGN-UPDATE]',
        'runSS_read': '[SSS-READ]'
    }

    data = {}


    for key in fileDir.keys():
        for fp in fileDir[key]:
            target = fp.split('_')[-1]
            target = target[0:target.find(".")]
            fp = open(fp).readlines()
            throughput = filter(lambda x: x.startswith("[OVERALL], Throughput"), fp)
            if key == 'load_' or key == 'loadSS_':
                latencyLoad = filter(lambda x: x.startswith(label[key]+', AverageLatency'), fp)
                if key not in data.keys():
                    data[key] = {'T':[], 'L':[], 'x':[]}
                data[key]['T'].append(throughput)
                data[key]['L'].append(latencyLoad)
                data[key]['x'].append(target)
            else:
                latencyUpdate = filter(lambda x: x.startswith(label[key+'update']+', AverageLatency'), fp)
                latencyRead = filter(lambda x: x.startswith(label[key+'read']+', AverageLatency'), fp)
                # Create keys for update/read because they share same run prefix
                if key not in data.keys():
                    data[key] = {'T':[], 'LR':[], 'LU':[], 'x':[]}

                data[key]['T'].append(throughput)
                data[key]['LR'].append(latencyRead)
                data[key]['LU'].append(latencyUpdate)
                data[key]['x'].append(target)

    return data


def get_file_dir(dataDir):

    fileDir = {'load_':[], 'loadSS_':[], 'run_':[], 'runSS_':[]}

    lsLtrOut = cmd.getoutput('ls -ltr '+dataDir)
    lsLtrOut = lsLtrOut.split('\n')

    for key in fileDir.keys():
        fileDir[key] = filter(lambda x: x.find(key) > 0, lsLtrOut)
        fileDir[key] = filter(lambda x: x.endswith('trace.txt') == False, fileDir[key])
        fileDir[key] = map(lambda  x: x[x.find(key):], fileDir[key])
        fileDir[key] = map(lambda  x: dataDir+x, fileDir[key])

    return fileDir

def clean_data(data):
    for key in data.keys():
        for label in data[key].keys():
            if label == 'T' or \
                            label == 'L' or \
                            label == 'LR'or \
                            label == 'LU':
                data[key][label] = itertools.chain(*data[key][label])
                data[key][label] = map(lambda x: x.rstrip('\n'), data[key][label])
                data[key][label] = map(lambda x: float(x.split(',')[-1]), data[key][label])

            elif label == 'x':
                data[key][label] = map(int, data[key][label])

    return data

def plot_data(data, outputDir):
        #TODO: add plot function
        plt.plot(data["load_"]['T'], data["load_"]['L'], 'r--',
                 data["loadSS_"]['T'], data["loadSS_"]['L'],'g^')
        plt.axis([0, 2000, 0, 2700])
        plt.show()





def main():
    parser = argparse.ArgumentParser(description="Produce delay throughput plot")
    parser.add_argument('-d',
                        '--dataDir',
                        type=str,
                        help='Data directory',
                        required=True)

    parser.add_argument('-o',
                        '--output',
                        type=str,
                        help='Output directory',
                        required=True)


    args = parser.parse_args()
    filesDir = get_file_dir(args.dataDir)

    data = proc_data(filesDir)
    data = clean_data(data)
    plot_data(data, args.output)





if __name__ == "__main__":
    main()