import argparse


def parse():
    parser = argparse.ArgumentParser(description='Download page')
    parser.add_argument("url")
    parser.add_argument(
        '--output',
        default='os.getcwd()',
        help='set output folder (default: current directory)',
    )
    return parser.parse_args()
