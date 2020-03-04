#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import logging
import sys

from tool.usernames import Usernames
from tool.assets import Assets
from tool.playout import play, catalogue_movies, catalogue_collections, catalogue_content
from tool.verbose import Verbose

users = Usernames()
assets = Assets()
verbose = Verbose()

logging.basicConfig(level=logging.INFO, format='%(message)s')


def get_parser():
    parser = argparse.ArgumentParser(description='Playout tool')
    parser.add_argument('--collections', action='store_true', default=False, help='Find collections in the catalogue')
    parser.add_argument('--crid', action='store', default='', help='Show crid details from the catalogue')
    parser.add_argument('--movies', action='store_true', default=False, help='Find playable movies in the catalogue')
    parser.add_argument('--with_cert', action='store', default='', help='Filter on certificate')
    parser.add_argument('--env', action='store', default='quality', help='Set for (integration or production)')
    parser.add_argument('-l', '--list_crids', action='store_true', default=False, help='List all QA crids')
    parser.add_argument('-v', '--verbose', action='store', default=0, type=int, help='Verbosity level of output')
    parser.add_argument('asset', action="store", nargs='*', help='Playout title|crid')

    return parser


def command_line_runner(argv=None):
    parser = get_parser()
    if argv is None:
        argv = sys.argv

    if len(argv) == 1:
        parser.print_usage()
        return

    args = parser.parse_args(argv[1:])

    if args.verbose:
        Verbose().set(level=args.verbose)

    # Show crid details
    if args.crid:
        catalogue_content(args.crid, args.env)
        return

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
        catalogue_movies(certificate=args.with_cert, env=args.env)
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
        if play(crid, env=args.env):
            print('Playable')
            return
        else:
            print('Not playable')
            return 1


if __name__ == '__main__':
    sys.exit(command_line_runner())
