import argparse
import os
import logging


def parse():
    logging.info('Parsing arguments')

    parser = argparse.ArgumentParser(description='Download page')
    parser.add_argument("url")
    parser.add_argument(
        '-o', '--output',
        default=os.getcwd(),
        help='set output folder (default: current directory)',
    )

    logging.info('Parsing finished')
    return parser.parse_args()
