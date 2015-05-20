__author__ = 'lex'
#Produces the paths needed from the cdfScript to run
import argparse
import commands
import os
import itertools


def get_data_files(input_dir):
    if input_dir.endswith('/'):
        input_dir = input_dir.rstrip('/')
    files = commands.getoutput('ls '+input_dir)
    files = files.split('\n')
    files = filter(lambda x: not x.endswith('trace.txt'), files)
    files = map(lambda x: input_dir+'/'+x, files)
    return files

def unique(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

def filter_keys(seq):
    if len(os.path.commonprefix((seq[0],seq[1]))) == 0:
        return False
    return True

def get_block_from_name(name):
    return name.split("_")[-2]

def get_output_name(output_path,label,block):
    if output_path.endswith('/'):
        return output_path+label[0]+block+'.pdf'
    else:
        return output_path+'/'+label[0]+block+'.pdf'

def match_files(input_files):
    common_prefix = os.path.commonprefix(input_files)
    no_dir_prefix = map(lambda x: x[len(common_prefix):], input_files)
    no_key_experiment = map(lambda x: x[x.find("_")+1:], no_dir_prefix)
    keys = map(lambda x: x[:x.find("_")+1], no_dir_prefix)
    keys = unique(keys)
    no_key_experiment = unique(no_key_experiment)
    key_combinations = [x for x in itertools.combinations(keys, 2)]
    key_combinations = filter(filter_keys, key_combinations)

    pairs = []
    for exp_suffix in no_key_experiment:
        for pair in key_combinations:
            pairs.append((pair[0]+exp_suffix,
                          pair[1]+exp_suffix))
    return pairs



def construct_script_lines(input_files, blocks, labels_load, labels_run, oPath):
    blueprint = "python cdfGen.py " \
                "-i %s %s " \
                "-l %s " \
                "-o %s " \
                "-f %s"
    file_pairs = match_files(input_files)
    common_prefix = os.path.commonprefix(input_files)

    for label in labels_load:
        for p in file_pairs:
            if p[0].startswith("load"):
                block = get_block_from_name(p[0])
                output_name = get_output_name(oPath,label,block)
                print blueprint % (common_prefix+p[0],common_prefix+p[1], label, output_name, block)

    for label in labels_run:
        for p in file_pairs:
            if p[0].startswith("run"):
                block = get_block_from_name(p[0])
                output_name = get_output_name(oPath,label,block)
                print blueprint % (common_prefix+p[0],common_prefix+p[1], label, output_name, block)

def main():
    parser = argparse.ArgumentParser(description="Creating the Script that produces CDF plots")
    parser.add_argument('-b', '--blocks',
                        type=int,
                        nargs='+',
                        help='Block Sizes in the experiment',
                        required=True)

    parser.add_argument('-i', '--input',
                        type=str,
                        help="Input data directory",
                        required=True)

    parser.add_argument('--lLoad', type=str, required=True,
                        nargs='+', help='Labels in the load files')

    parser.add_argument('--lRun', type=str, required=True, nargs='+',
                        help="Labels in the Run files")

    parser.add_argument('-o','--output', type=str, required=True,
                        help="Output file path")
    args = parser.parse_args()

    data_files = get_data_files(args.input)
    script_lines = \
        construct_script_lines(data_files, args.blocks,
                               args.lLoad, args.lRun, args.output)


if __name__ == "__main__":
    main()