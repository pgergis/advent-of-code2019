import argparse
from utils.file_parser import get_lines_from_path

parser = argparse.ArgumentParser(description="Provide an input file.")
parser.add_argument(
    "file_in",
    metavar="file",
    type=str,
    help="the path to the file containing the input to the problem",
)

args = parser.parse_args()
file_in = args.file_in
lines_in = get_lines_from_path(file_in)
