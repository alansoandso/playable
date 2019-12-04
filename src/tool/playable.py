#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import logging
import sys

from tool.usernames import Usernames
from tool.assets import Assets
from tool.playout import play, catalogue_movies, catalogue_collections
from tool.verbose import Verbose

users = Usernames()
assets = Assets()
verbose = Verbose()

logging.basicConfig(level=logging.INFO, format='%(message)s')


def parse_args(argv):
    parser = argparse.ArgumentParser(description='Playout tool')
    parser.add_argument('--collections', action='store_true', default=False, help='Find collections in the catalogue')
    parser.add_argument('--movies', action='store_true', default=False, help='Find playable movies in the catalogue')
    parser.add_argument('--with_cert', action='store', default='', help='Filter on cerrtificate')
    parser.add_argument('--env', action='store', default='qa', help='Override environment with (integration or production)')
    parser.add_argument('-l', '--list_crids', action='store_true', default=False, help='List all QA crids')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='verbose')
    parser.add_argument('asset', action="store", nargs='*', help='Playout title|crid')

    if len(argv) == 1:
        parser.print_usage()
        exit(1)
    else:
        return parser.parse_args(argv[1:])


def command_line_runner(argv=None):
    if argv is None:
        argv = sys.argv

    args = parse_args(argv)

    if args.verbose:
        Verbose().set()

    # List all QA crids
    if args.list_crids:
        assets.list_titles()
        return

    # Find collections in the catalogue
    if args.collections:
        catalogue_collections(args.env)
        return

    # Find playable movies in the catalogue
    if args.movies:
        catalogue_movies(certificate=args.with_cert)
        return

    # Playout title|crid
    if args.asset:
        # asset can be a crid or a title
        crid = assets.get_crid(' '.join(args.asset))
        x = ' '.join(args.asset)
        print(f'Looking for: {x}')

        if not crid:
            crid = args.asset[0]

        print(f'Using: {crid}')
        if play(crid):
            print('OK')


if __name__ == '__main__':
    sys.exit(command_line_runner())
