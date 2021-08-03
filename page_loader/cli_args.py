from page_loader.logger import logging_info
import argparse
import os


@logging_info('Parsing arguments')
def parse():
    parser = argparse.ArgumentParser(description='Download page')
    parser.add_argument("url")
    parser.add_argument(
        '-o', '--output',
        default=os.getcwd(),
        help='set output folder (default: current directory)',
    )

    return parser.parse_args()
