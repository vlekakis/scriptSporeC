__author__ = 'lex'

# Produces the throughput latency plot

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
        fileDir[key] = map(lambda x: x[x.find(key):], fileDir[key])
        fileDir[key] = map(lambda x: dataDir+x, fileDir[key])

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

def plot_data(data, output_directory, key, key_signature, filename, label_redis, label_signature):

        if key == "load_":
            plt.plot(data[key]['T'], data[key]['L'], 'bo--', label=label_redis)
            plt.plot(data[key_signature]['T'], data[key_signature]['L'],'go--',label=label_signature)

            plt.axis([0,
                  max(data[key]['x'])+100,
                  0,
                  max([
                      max(data[key]['L']),
                      max(data[key_signature]['L'])]
                  )+100])
        else:
            plt.plot(data[key]['T'], data[key]['LR'], 'bo--', label=label_redis+'-Read')
            plt.plot(data[key]['T'], data[key]['LU'], 'bD--', label=label_redis+'-Update')
            plt.plot(data[key_signature]['T'], data[key]['LR'], 'go--', label=label_redis+'-Read')
            plt.plot(data[key_signature]['T'], data[key]['LU'], 'gD--', label=label_redis+'-Update')



        plt.ylabel("Delay (usec)")
        plt.xlabel("Operations (op/sec)")
        plt.legend()
        plt.savefig(output_directory+'/'+filename)
        plt.clf()



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

    plot_data(data, args.output, "load_", "loadSS_", "load.pdf", "redis-vanilla", "redis-signature")
    plot_data(data, args.output, "run_", "runSS_", "run.pdf", "redis-vanilla", "redis-signature")

if __name__ == "__main__":
    main()