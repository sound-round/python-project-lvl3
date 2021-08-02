#!/usr/bin/env python3


from page_loader import page_loader
from page_loader import cli_args
import logging
import argparse
import sys


def main():
    logging.basicConfig(
        filename='log.log',
        filemode='w',
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p',
    )
    console = logging.StreamHandler()
    console.setLevel(logging.ERROR)

    logging.info('Started')

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

    logging.info('Finished')
    sys.exit()


if __name__ == '__main__':
    main()
