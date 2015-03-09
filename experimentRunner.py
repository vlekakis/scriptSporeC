__author__ = 'lex'
import argparse
import os
import shutil
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

    parser.add_argument('--dryRun',
                        action='store_true',
                        default=False)



    args = parser.parse_args()

    result_dir_name = args.output +'_'+ str(date.today())
    if os.path.exists(result_dir_name):
        print 'Given directory exists, deleting...'
        shutil.rmtree(result_dir_name)

    print 'Creating output directory'
    os.mkdir(result_dir_name)

    cmd = "%s %s %s -s -P %s > %s"
    modes = ['load', 'run']
    for client in args.clients:
        for workload in args.workloads:
            for mode in modes:

                o_dir = result_dir_name
                w_path = args.input
                if w_path.endswith('/') == False:
                    w_path += '/'
                w_path += workload
                if o_dir.endswith('/') == False:
                    o_dir += '/'
                o_dir+=mode+'_'+client+'_'+workload+'.txt'

                run_cmd = cmd % (args.bin, mode, client, w_path, o_dir)
                print "= = = = = = = = = = = = = = = = = = = ="
                print "Running ", mode, " for client",  client, "and workload", workload
                print "= = = = = = = = = = = = = = = = = = = ="
                if args.dryRun:
                    print run_cmd
                else:
                    os.system(run_cmd)



if __name__ == "__main__":
    main()