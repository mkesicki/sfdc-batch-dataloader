#!/usr/bin/python3 -u

import argparse
import pprint

import sfdc

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description = 'Import salesforce data for Numberly (via CSV file).')
    parser.add_argument('login_url', metavar = 'login_url', help = 'Login url to Salesforce (production or sandbox)')
    parser.add_argument('client_id', metavar = 'client_id', help = 'Salesforce application client_id used to login')
    parser.add_argument('client_secret', metavar = 'client_secret', help = 'Salesforce application client_secret used to login')
    parser.add_argument('username', metavar = 'username', help = 'User name for login')
    parser.add_argument('password', metavar = 'password', help = 'User password for login')
    parser.add_argument('path', metavar = 'path', help = 'Path to Data Loader')
    parser.add_argument('object', metavar = 'object', help = 'Salesforce object to backup')
    parser.add_argument('--fields', metavar = 'fields', help = 'Coma separated list of fields to export, all if not selected')
    args = parser.parse_args()

    pprint.pprint(args)

    instance_url = sfdc.login(args)
