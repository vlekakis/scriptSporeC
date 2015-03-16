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

    args = parser.parse_args()


    result_dir_name = args.output +'_'+ str(date.today())
    if len(args.extraText) > 0:
        result_dir_name += '_'+args.extraText

    if os.path.exists(result_dir_name) == False:
        print 'Given directory exists, deleting...'
        os.mkdir(result_dir_name)

    cmd = ""
    if args.timeseries == False:
        cmd = "%s %s %s -s -p fieldlength=%s -P %s > %s 2>%s"
    else:
        cmd =  "%s %s %s -s -p fieldlength=%s "
        cmd += "-p measurementtype=timeseries -p timeseries.granularity=%s  -P %s > %s 2>%s"

    #
    modes = ['load', 'run']
    for client in args.clients:
        for workload in args.workloads:
            for fieldLen in args.fLengths:
                for mode in modes:

                    o_dir = result_dir_name
                    trace_track = result_dir_name
                    w_path = args.input
                    if w_path.endswith('/') == False:
                        w_path += '/'
                    w_path += workload
                    if o_dir.endswith('/') == False:
                        o_dir += '/'
                    if trace_track.endswith('/') == False:
                        trace_track+= '/'

                    o_dir+=mode+'_'+client+'_'+workload+'_'+fieldLen+'.txt'
                    trace_track+=mode+'_'+client+'_'+workload+'_'+fieldLen+'_trace.txt'
                    run_cmd = ""
                    if args.timeseries == False:
                        run_cmd = cmd % (args.bin, mode, client,
                                         fieldLen, w_path, o_dir, trace_track)
                    else:
                        run_cmd = cmd % (args.bin, mode, client,
                                         fieldLen, args.granularity,
                                         w_path, o_dir, trace_track)

                    print "= = = = = = = = = = = = = = = = = = = ="
                    print "Running ", mode, " for client",  client, "and workload", workload, "field", fieldLen
                    print "= = = = = = = = = = = = = = = = = = = ="
                    if args.dryRun:
                        print run_cmd
                    else:
                        os.system(run_cmd)



if __name__ == "__main__":
    main()
