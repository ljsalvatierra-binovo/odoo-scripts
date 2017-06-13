# -*- coding: utf-8 -*-
# !/usr/bin/env python3
#
# Python script to install require Odoo addons
#
# Copyright (C) 2017 Binovo IT Human Project S.L.
#
# Author: Luis J. Salvatierra

from __future__ import print_function
from getpass import getpass
import os
import argparse
import erppeek


class OdooAPI:
    def __init__(self,
                 url='http://localhost:8069',
                 database=None,
                 user='admin',
                 password='admin',
                 verbosity=False):
        srv, db = url, database
        user, pwd = user, password
        self.api = erppeek.Client(srv, db, user, pwd, transport=None, verbose=verbosity)

    def module_exists(self, name, installed=None):
        modules = self.api.modules(name)
        print(modules)
        if not modules:
            return False
        if installed is None:
            if name in modules['installed'] or name in modules['uninstalled']:
                return True
            else:
                return False
        if installed and 'installed' in modules:
            return name in modules['installed']
        elif not installed and 'uninstalled' in modules:
            return name in modules['uninstalled']

    def install_addons(self, addons_list):
        if 0 == len(addons_list):
            print('Empty addons list.')
            return False
        addons_non_installed = []
        addons_installed = []
        for addon in addons_list:
            if not api.module_exists(name=addon, installed=True):
                addons_non_installed.append(addon)
            else:
                addons_installed.append(addon)
        if 0 < len(addons_installed):
            addons_installed.sort()
            for module in addons_installed:
                print('%s is already installed.' % module)
        if 0 < len(addons_non_installed):
            addons_non_installed.sort()
            print('Modules to install:')
            print(', '.join(addons_non_installed))
            print('%s modules to be installed.' % len(addons_non_installed))
            key = input('Do you wish to continue? [Y/n] ')
            if 'Y' == key.upper():
                for addon in addons_non_installed:
                    api.api.install(addon)
                print('%s modules installed.' % len(addons_non_installed))
                print('It is recommended to update the module list in Odoo and run again.')
            elif 'N' == key.upper():
                print('Bye!')
            else:
                print('Key "%s" not recognised.' % key)
        else:
            print('%s modules to be installed.' % len(addons_non_installed))
        return True

    def uninstall_addons(self, addons_list):
        if 0 == len(addons_list):
            print('EMpty addons list.')
            return False
        addons_non_installed = []
        addons_to_uninstall = []
        for addon in addons_list:
            if not api.module_exists(name=addon, installed=True):
                addons_non_installed.append(addon)
            else:

                addons_to_uninstall.append(addon)
        if 0 < len(addons_to_uninstall):
            addons_to_uninstall.sort()
            print('Modules to uninstall:')
            print("\n".join(addons_to_uninstall))
            print('%s modules to be uninstalled.' % len(addons_to_uninstall))
            key = input('Do you wish to continue? [Y/n] ')
            if 'Y' == key.upper():
                for addon in addons_non_installed:
                    api.api.uninstall(addon)
            else:
                print('Bye!')
        return True


class AddonPath:
    def __init__(self, path=None):
        self.path = path
        self.addons = self.get_existing_addons(path)

    @staticmethod
    def get_existing_addons(path):
        try:
            contents = os.listdir(path)
            dirs = []
            for c in contents:
                if os.path.isdir(os.path.join(c, path)):
                    dirs.append(c)
        except OSError as e:
            print(e)
            exit(-1)
        return dirs


def check_non_existing_addons(paths=[], addons_list=[]):
    addon_dir = []
    existing_addons = []
    non_existing_addons = []
    for path in paths:
        print("Checking existing addons in '%s'" % os.path.abspath(path))
        addon_path = AddonPath(path=os.path.abspath(path))
        addon_dir += addon_path.addons
    for addon in addons_list:
        if addon in addon_dir:
            existing_addons.append(addon)
        else:
            non_existing_addons.append(addon)
    if 0 < len(non_existing_addons):
        print('Modules to download:')
        print(','.join(non_existing_addons))
        print('%d modules need to be downloaded.' % len(non_existing_addons))
        return True
    return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--install', action='store_true', help='Install all the specified addons.')
    parser.add_argument('-u', '--uninstall', action='store_true', help='Uninstall all the specified addons.')
    parser.add_argument('-p', '--addons-paths-list-file',
                        default=None, help='All Odoo addons paths.')
    parser.add_argument('-a', '--addons-list-file',
                        default=None, help='Addons list to install.')
    parser.add_argument('-d', '--db', default=None, help='DB name.')
    parser.add_argument('--user', default=None, help='DB user.')
    parser.add_argument('--password', default=None, help='DB password.')
    parser.add_argument('--url', default='http://localhost:8069', help='Web App URL.')
    parser.add_argument('--verbosity', default=False, help='Verbosity.')
    args = parser.parse_args()
    try:
        if args.install and args.uninstall:
            print('Please, select install OR uninstall, not both!')
            exit(1)
        if not args.install and not args.uninstall:
            print('Please, select install OR uninstall.')
            exit(1)
        if args.addons_list_file is None:
            addons_list_file = input('Addon/Module list file path: ')
            if '' == addons_list_file:
                print('Bye!')
                exit(1)
        else:
            addons_list_file = args.addons_list_file
        if not os.path.isfile(addons_list_file):
            print('The file does not exist. Bye!')
            exit(1)
        addons_list = []
        with open(addons_list_file, 'r') as f:
            for line in f:
                addons_list.append(line.rstrip('\n'))
        if args.install:
            if args.addons_paths_list_file is None:
                addons_paths_list_file = input('Insert Odoo addons_path_list file path: ')
                if '' == addons_paths_list_file:
                    print('Bye!')
                    exit(1)
            else:
                addons_paths_list_file = args.addons_paths_list_file
            if not os.path.isfile(addons_paths_list_file):
                print('The file does not exist. Bye!')
                exit(1)
            addons_paths_list = []
            with open(addons_paths_list_file, 'r') as f:
                for line in f:
                    addons_paths_list.append(line.rstrip('\n'))
            if check_non_existing_addons(paths=addons_paths_list, addons_list=addons_list):
                print('Bye!')
                exit(1)
        if args.db is None:
            dbname = input('Insert PostgreSql DB name: ')
            if '' == dbname:
                print('Bye!')
                exit(1)
        else:
            dbname = args.db
        if args.user is None:
            dbuser = input('DB user: ')
            if '' == dbuser:
                print('Bye!')
                exit(1)
        else:
            dbuser = args.user
        if args.password is None:
            dbpass = getpass('DB pass: ')
            if '' == dbpass:
                print('Bye!')
                exit(1)
        else:
            dbpass = args.password
        api = OdooAPI(url=args.url,
                      database=dbname,
                      user=dbuser,
                      password=dbpass,
                      verbosity=args.verbosity)
        if args.uninstall:
            api.uninstall_addons(addons_list)
        else:
            api.install_addons(addons_list)
    except erppeek.Error as eperr:
        print(eperr)
    except ConnectionRefusedError as cre:
        print(cre)
    except KeyboardInterrupt:
        print('\nBye!')
        exit(1)
