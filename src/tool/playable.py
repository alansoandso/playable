#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import logging
import sys

from user.mongo import Mongo
from user.usernames import Usernames
users = Usernames()

logging.basicConfig(level=logging.INFO, format='%(message)s')


def parse_args(argv):
    parser = argparse.ArgumentParser(description='Playout tool')
    parser.add_argument('-l', '--list_crids', action='store_true', default=False, help='List all QA crids')
    parser.add_argument('asset', action="store", nargs='?', help='title or crid')

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
        users.list_usernames()
        return

    if args.user:
        profileid = users.get_profileid(args.user)
        if profileid:
            print(get_records(profileid, args))
            return


def get_records(profileid, include):
    mongo = Mongo(profileid)
    report = ''
    report += mongo.get_accounts()
    report += mongo.get_entitlements()

    if include.atv or include.all:
        report += mongo.get_atv_subscriptions()

    if include.vodafone or include.all:
        report += mongo.get_vodafone_accounts()
    return report


if __name__ == '__main__':
    sys.exit(command_line_runner())
