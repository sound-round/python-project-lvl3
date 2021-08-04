from page_loader.logger import logging_info
import argparse
import os
import pkg_resources


version = pkg_resources.get_distribution('hexlet-code').version


@logging_info('Parsing arguments')
def parse():
    parser = argparse.ArgumentParser(description='Download the page')
    parser.add_argument('url', help='url of the page')
    parser.add_argument(
        '-V', '--version',
        help='output the version number',
        action='version',
        version=version
    )
    parser.add_argument(
        '-o', '--output',
        default=os.getcwd(),
        help='set output folder (default: "/app")',
    )

    return parser.parse_args()
