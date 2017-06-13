# -*- coding: utf-8 -*-
# !/usr/bin/python3
#
# Python script to install require Odoo addons
#
# Copyright (C) 2017 Binovo IT Human Project S.L.
#
# Author: Luis J. Salvatierra
from __future__ import print_function
import csv
import argparse

DELIMITER = ','


def prepare_csv_data(csv_file):
    """Parse a decoded CSV file and return head list and data list

    :param csv_file: decoded CSV file
    :param delimiter: CSV file delimiter char
    :returns: (head [list of first row], data [list of list])

    """
    try:
        with open(csv_file, encoding='utf-8') as fp:
            data = csv.DictReader(fp, delimiter=DELIMITER)
            fields = data.fieldnames
            rows = [x for x in data]
    except csv.Error as error:
        print('CSV file is malformed, maybe you have not choose correct separator.')
        print(error.message)
        return False, False
    return fields, rows


if '__main__' == __name__:
    parser = argparse.ArgumentParser(
        description='Compare 2 csv file of Odoo Addon list. It must contain the addon technical name.'
    )
    parser.add_argument('csv1', type=str, metavar='1.csv')
    parser.add_argument('csv2', type=str, metavar='2.csv')
    args = parser.parse_args()
    try:
        fields1, data1 = prepare_csv_data(args.csv1)
        fields2, data2 = prepare_csv_data(args.csv2)
        technical_name_list1 = []
        technical_name_list2 = []
        if 'Nombre técnico' in fields1 and 'Nombre técnico' in fields2:
            idx = 'Nombre técnico'
        elif 'Technical name' in fields1 and 'Technical name' in fields2:
            idx = 'Technical name'
        else:
            print("No 'Technical name' column found.")
            exit(1)
        for row in data1:
            technical_name_list1.append(row[idx])
        for row in data2:
            technical_name_list2.append(row[idx])
        technical_name_list1.sort()
        technical_name_list2.sort()
        addons_1_not_in_2 = []
        addons_2_not_in_1 = []
        for addon in technical_name_list1:
            if addon not in technical_name_list2:
                addons_1_not_in_2.append(addon)
        for addon in technical_name_list2:
            if addon not in technical_name_list1:
                addons_2_not_in_1.append(addon)
        print('%s addons (%d) not in %s:' % (args.csv1, len(addons_1_not_in_2), args.csv2))
        print("\n".join(addons_1_not_in_2))
        print('%s addons (%d) not in %s:' % (args.csv2, len(addons_2_not_in_1), args.csv1))
        print("\n".join(addons_2_not_in_1))
    except KeyboardInterrupt:
        print('Bye!')
        exit(1)