#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import logging
import sys

from tool.usernames import Usernames
from tool.assets import Assets
from tool.playout import play

users = Usernames()
assets = Assets()

logging.basicConfig(level=logging.INFO, format='%(message)s')


def parse_args(argv):
    parser = argparse.ArgumentParser(description='Playout tool')
    parser.add_argument('-l', '--list_crids', action='store_true', default=False, help='List all QA crids')
    parser.add_argument('asset', action="store", nargs='*', help='title or crid')

    if len(argv) == 1:
        parser.print_usage()
        exit(1)
    else:
        return parser.parse_args(argv[1:])


def command_line_runner(argv=None):
    if argv is None:
        argv = sys.argv

    args = parse_args(argv)

    # List all QA crids
    if args.list_crids:
        assets.list_titles()
        return

    if args.asset:
        # asset can be a crid or a title
        crid = assets.get_crid(' '.join(args.asset))
        x = ' '.join(args.asset)
        print(f'Looking for >{x}<')
        if not crid:
            crid = args.asset[0]
        return play(crid)


if __name__ == '__main__':
    sys.exit(command_line_runner())
