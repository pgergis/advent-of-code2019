import argparse

parser = argparse.ArgumentParser(description='Provide an input file.')
parser.add_argument('file_in', metavar='file', type=str, help='the path to the file containing the input to the problem')

args = parser.parse_args()
file_in = args.file_in

with open(file_in, 'r') as input_f:
    lines_in = input_f.readlines()
