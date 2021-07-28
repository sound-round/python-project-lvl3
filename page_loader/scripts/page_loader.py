#!/usr/bin/env python3


from page_loader import page_loader
from page_loader import cli_args
import logging
import argparse


def main():
    logging.basicConfig(
        filename='log.log',
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p',
    )
    logging.info('Started')

    try:
        args = cli_args.parse()
    except argparse.ArgumentError:
        logging.warning('URL is missing')
    else:
        file_path = page_loader.download(args.url, args.output)
        print('Page was successfully downloaded into', f"\'{file_path}\'")

    logging.info('Finished')


if __name__ == '__main__':
    main()
