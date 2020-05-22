#!/usr/bin/python3 -u

import argparse
import pprint
import sfdc
import os
import subprocess

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description = 'Backup salesforce data')
    parser.add_argument('login_url', metavar = 'login_url', help = 'Login url to Salesforce (production or sandbox)')
    parser.add_argument('client_id', metavar = 'client_id', help = 'Salesforce application client_id used to login')
    parser.add_argument('client_secret', metavar = 'client_secret', help = 'Salesforce application client_secret used to login')
    parser.add_argument('username', metavar = 'username', help = 'User name for login')
    parser.add_argument('password', metavar = 'password', help = 'User password for login')
    parser.add_argument('path', metavar = 'path', help = 'Absolute path to Data Loader *.uber.jar file')
    parser.add_argument('object', metavar = 'object', help = 'Salesforce object to backup')
    parser.add_argument('--fields', metavar = 'fields', help = 'Coma separated list of fields to export, all if not selected')
    args = parser.parse_args()

    instance_url = sfdc.login(args)

    if args.fields is not None:
        fields = args.fields.split(',')
    else:
        fields = sfdc.getFields(args.object)

    pwd = os.path.dirname(os.path.realpath(__file__))
    path = args.path
    key_file = pwd + "\\key\\" + "key.key"

    print("Encrypt password...")

    subprocess.run(["java", "-cp", path, "com.salesforce.dataloader.security.EncryptionUtil", "-k", key_file], check=True)
    result = subprocess.run(["java", "-cp", path, "com.salesforce.dataloader.security.EncryptionUtil", "-e", args.password, key_file], check=True)
    # pprint.pprint(x)
    # print( result.stdout)
