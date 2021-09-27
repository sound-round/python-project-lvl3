#!/usr/bin/env python3


from page_loader import page_loader
from page_loader import cli_args
from page_loader.logger import configure_logging, configure_console
import logging
import sys


def main():
    configure_logging()
    console = configure_console()

    try:
        args = cli_args.parse()
        file_path = page_loader.download(args.url, args.output)
        print('Page was successfully downloaded into', f"\'{file_path}\'")
        sys.exit()
    except (
            Exception
    ) as e:
        logging.error(console, e)
        sys.exit(1)


if __name__ == '__main__':
    main()
