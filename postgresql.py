# -*- coding: utf-8 -*-
# !/usr/bin/env python
#
# Python script to install require Odoo addons
#
# Copyright (C) 2017 Binovo IT Human Project S.L.
#
# Author: Luis J. Salvatierra
import psycopg2
from pprint import pprint


def _pg_stat_statements(db, user, password, host, port):
    sql = """
        SELECT query, calls, total_time / 1000.0, rows, 100.0 * shared_blks_hit /
            nullif(shared_blks_hit + shared_blks_read, 0) AS hit_percent
        FROM pg_stat_statements
        ORDER BY total_time DESC LIMIT 5;
        """
    conn = psycopg2.connect(
        host=host, port=port, user=user, password=password, database=db
    )
    cur = conn.cursor()
    cur.execute(sql)
    res = cur.fetchall()
    pprint(res)


def _run_test(db, user, password, host, port):
    pass


def _ir_translation_word_count(db, user, password, host, port, lang):
    conn = psycopg2.connect(
        host=host, port=port, user=user, password=password, database=db
    )
    cur = conn.cursor()
    sql = """
        SELECT DISTINCT(src) FROM ir_translation WHERE lang = %s
    """
    cur.execute(sql, (lang,))
    src_words_fetched = cur.fetchall()
    res = 0
    for line in src_words_fetched:
        words = line[0].split() if line and isinstance(line, tuple) and 0 < len(line) and line[0] else []
        big_words = [word for word in words if 3 < len(word)]
        res += len(big_words)
    return res


try:
    db = 'binovo'
    user = 'admin'
    password = 'admin'
    host = '127.0.0.1'
    port = 5432

    _pg_stat_statements(db, user, password, host, port)

    _run_test(db, user, password, host, port)

except Exception, e:
    print(e.message)
