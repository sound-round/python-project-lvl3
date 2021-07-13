import argparse


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--output',
        default='os.getcwd()',
        help='set output folder (default: current directory)',
    )
    return parser.parse_args()