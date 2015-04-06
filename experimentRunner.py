__author__ = 'lex'
import argparse
import os
from datetime import date


def main():
    parser = argparse.ArgumentParser(description="Experiment runner")
    parser.add_argument('-c',
                        '--clients',
                        type=str,
                        nargs='+',
                        help='YCSB clients',
                        required=True)

    parser.add_argument('-w',
                        '--workloads',
                        type=str,
                        nargs='+',
                        help='YCSB workloads',
                        required=True)

    parser.add_argument('-o',
                        '--output',
                        type=str,
                        help='Output Directory',
                        required=True)

    parser.add_argument('-i',
                        '--input',
                        type=str,
                        help='Workloads input directory',
                        required=True)

    parser.add_argument('-b',
                        '--bin',
                        type=str,
                        help='YCSB binary path',
                        required=True)

    parser.add_argument('-f',
                        '--fLengths',
                        type=str,
                        nargs='+',
                        help='Field length',
                        required=True)

    parser.add_argument('--dryRun',
                        action='store_true',
                        default=False)

    parser.add_argument('--extraText',
                        type=str,
                        default="",
                        help="Extra text to identify the run")

    parser.add_argument('-t',
                        '--timeseries',
                        action='store_true',
                        default=False)

    parser.add_argument('-g',
                        '--granularity',
                        type=str,
                        default="5000",
                        help="Timeseries granularity")

    parser.add_argument('-m',
                        '--modes',
                        help='Modes to Run for given clients',
                        type=str,
                        nargs='+',
                        required=True)

    parser.add_argument('--target',
                        default='',
                        type=str,
                        nargs='+',
                        help='Target throughput for the experiment')

    parser.add_argument('--thread',
                        default=1,
                        type=int,
                        help='Number of execution threads')

    args = parser.parse_args()

    result_dir_name = args.output + '_' + str(date.today())
    if len(args.extraText) > 0:
        result_dir_name += '_' + args.extraText

    if os.path.exists(result_dir_name) == False:
        print 'Given directory exists, deleting...'
        os.mkdir(result_dir_name)

    propertyCmd = ""
    cmdPrefix = "%s %s %s -s -p fieldlength=%s "
    cmdSuffix = "-P %s > %s 2>%s"
    targetEnabled = False


    if len(args.target) > 0:
        targetEnabled = True
        propertyCmd +=  "-target %s "
    else:
        args.target = ['unlimited']


    if args.thread > 1:
        threadStr = "-threads %d " % (args.thread)
        propertyCmd += threadStr

    if args.timeseries == True:
        propertyCmd += "-p measurementtype=timeseries -p timeseries.granularity=%s "

    cmd = cmdPrefix + propertyCmd + cmdSuffix
    for client in args.clients:
        for workload in args.workloads:
            for fieldLen in args.fLengths:
                for target in args.target:
                    for mode in args.modes:

                        o_dir = result_dir_name
                        trace_track = result_dir_name
                        w_path = args.input
                        if w_path.endswith('/') == False:
                            w_path += '/'
                        w_path += workload
                        if o_dir.endswith('/') == False:
                            o_dir += '/'
                        if trace_track.endswith('/') == False:
                            trace_track += '/'


                        o_dir += mode + '_' \
                                 + client + '_' \
                                 + workload + '_' \
                                 + fieldLen + '_'\
                                 + target + '.txt'

                        trace_track += mode + '_' \
                                       + client + '_' \
                                       + workload + '_'\
                                       + fieldLen + '_'\
                                        +target + '_trace.txt'
                        run_cmd = ""

                        if args.timeseries == False and targetEnabled == False:
                            run_cmd = cmd % (args.bin, mode, client,
                                             fieldLen, w_path, o_dir, trace_track)

                        elif args.timeseries == True and targetEnabled == False:
                            run_cmd = cmd % (args.bin, mode, client,
                                             fieldLen, args.granularity,
                                             w_path, o_dir, trace_track)

                        elif args.timeseries == False and targetEnabled == True:
                            run_cmd = cmd % (args.bin, mode, client,
                                             target,
                                             fieldLen, w_path, o_dir, trace_track)
                        else:
                            run_cmd = cmd % (args.bin, mode, client, target,
                                             fieldLen, args.granularity,
                                             w_path, o_dir, trace_track)


                        print "= = = = = = = = = = = = = = = = = = = ="
                        print "Running ", mode, " for client", client, "and workload", workload, "field", fieldLen
                        print "= = = = = = = = = = = = = = = = = = = ="
                        if args.dryRun:
                            print run_cmd
                        else:
                            os.system(run_cmd)


if __name__ == "__main__":
    main()
