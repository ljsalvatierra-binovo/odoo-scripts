# -*- coding: utf-8 -*-
# !/usr/bin/env python
#
# Python script to install require Odoo addons
#
# Copyright (C) 2017 Binovo IT Human Project S.L.
#
# Author: Luis J. Salvatierra

from __future__ import print_function
import erppeek


if '__main__' == __name__:
    srv, db = 'http://localhost:8069', 'binovo'
    user, pwd = 'admin', 'admin'
    api = erppeek.Client(srv, db, user, pwd, transport=None, verbose=False)

    try:
        model = api.model('res.partner')
        list_ids = [1, 2, 3, 4]
        domain = ['|', ('field1', '=', True), ('field2', 'in', [list_ids])]
        model_browse_objs = model.browse(domain=domain)  # <RecordList 'model.name,length=X'>
        model_search_objs = model.search(domain)  # List of Ids
        fields = ['field1', 'field2', '...']
        model_browse_fields_objs = model_browse_objs.read(fields=fields)  # List of dictionaries
    except erppeek.Error as e:
        print(e)
