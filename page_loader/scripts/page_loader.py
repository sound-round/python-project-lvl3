#!/usr/bin/env python3


from page_loader import page_loader
from page_loader import cli_args


def main():
    args = cli_args.parse()
    file_path = page_loader.download(args.url, args.output)
    print(file_path)


if __name__ == '__main__':
    main()
