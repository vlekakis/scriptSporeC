__author__ = 'lex'

import argparse
import json

def extract_metric_unit(dirtyMUnit):
    dirtyMUnit = dirtyMUnit.rstrip()
    dirtyMUnit = dirtyMUnit.lstrip()
    if dirtyMUnit.find('(') < 0:
        if dirtyMUnit.isdigit():
            return [dirtyMUnit, -1]
        elif dirtyMUnit.startswith('>'):
            return [dirtyMUnit[1:], -1]

        else:
            return [dirtyMUnit, None]
    else:
        sIndex = dirtyMUnit.index('(')
        eIndex = dirtyMUnit.index(')')
        metric = dirtyMUnit[0:sIndex]
        unit = dirtyMUnit[sIndex+1:eIndex]
        return [metric,unit]

def extract_measurement_label(dirtyLabel):
    sIndex = dirtyLabel.find('[')
    eIndex = dirtyLabel.find(']')
    if sIndex > -1 and eIndex > -1:
        return dirtyLabel[sIndex+1:eIndex]
    return ""

def extract_data(input):
    data = {}
    for line in input:
        if line.startswith("YCSB Client"):
            continue
        if line.startswith("Command line:"):
            continue
        if line.startswith("java -cp"):
            continue

        line = line.rstrip('\n')
        line_parts = line.split(',')
        if len(line_parts) == 3:
            mlabel = extract_measurement_label(line_parts[0])
            if mlabel not in data.keys():
                data[mlabel] = dict()
                data[mlabel]['dat'] = dict()

            metric, unit = extract_metric_unit(line_parts[1])
            if unit == -1:
                data_point = int(metric)
                data[mlabel]['dat'][data_point] = int(line_parts[2])

            elif metric.startswith('Return'):
                print 'Info', line

            elif unit == None:
                data[mlabel][metric] =  {"unit":unit, "data":line_parts[2]}



        else:
            print "Line with less than 3 arguments"
            print line
    return data

def main():
    parser = argparse.ArgumentParser(description="Data extraction script")
    parser.add_argument('-i', '--input', type=file, help='Input file', required=True)
    parser.add_argument('-o', '--output', type=str, help='Output file', required=True)
    parser.add_argument('-t', '--type', type=str,
                        choices=('Histogram', 'Timeseries'),
                        help="Type of input data",
                        required=True)

    try:
        args = parser.parse_args()
    except IOError as e:
        print "Input parameter should be a file"


    data = extract_data(args.input)
    fp = open(args.output, 'w')
    json.dump(data,fp)
    fp.close()



if __name__ == "__main__":
    main()