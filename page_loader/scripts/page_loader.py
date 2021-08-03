#!/usr/bin/env python3


from page_loader import page_loader
from page_loader import cli_args
from page_loader.logger import configure_logging
import logging
import argparse
import sys


def main():
    configure_logging()
    logging.info('Downloading started')

    try:
        args = cli_args.parse()
    except argparse.ArgumentError as e:
        logging.warning(e)
        raise
    else:
        try:
            file_path = page_loader.download(args.url, args.output)
        except (
                Exception
        ) as e:
            logging.error(console, e)
            sys.exit(1)
        else:
            print('Page was successfully downloaded into', f"\'{file_path}\'")

    logging.info('Downloading finished')
    sys.exit()


if __name__ == '__main__':
    main()
