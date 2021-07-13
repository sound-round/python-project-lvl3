#!/usr/bin/env python3


from page_loader import loader
from page_loader import cli_args


def main():
    args = cli_args.parse()
    file_path = loader.download(args.output)
    print(file_path)


if __name__ == '__main__':
    main()