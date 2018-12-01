# Copyright (c) 2013, Libermatic and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from datetime import datetime
from functools import partial, reduce
from operator import add
from toolz import compose, assoc, get, concatv, merge, pluck


def execute(filters=None):
    return get_columns(), compose(
        partial(map, make_row)
    )(get_data(filters))


def get_columns():
    return [
        'Sales Invoice:Link/Sales Invoice:120',
        'Patient ID:Link/Patient:90',
        'Time:Datetime:150',
        'Amount:Currency:90',
        'Discount:Currency:90',
        'Total:Currency:90',
        'Paid:Currency:90',
        'Outstanding:Currency:90',
        'Commission:Currency:90',
        'Sales Partner:Link/Sales Partner:120',
    ]


def add_filter_clause(filters, field):
    def fn(clauses):
        if filters.get(field):
            clause = ['{field}=%({field})s'.format(field=field)]
            return concatv(clauses, clause)
        return clauses
    return fn


def add_filter_value(filters, field):
    def fn(values):
        if filters.get(field):
            value = {field: filters.get(field)}
            return merge(values, value)
        return values
    return fn


def make_filter_composer(filters, fields):
    def fn(add_fn):
        return compose(
            *map(
                lambda field: add_fn(filters, field),
                fields,
            )
        )
    return fn


def make_conditions(filters):
    init_clauses = [
        'docstatus=1',
        'posting_date BETWEEN %(from_date)s AND %(to_date)s',
    ]
    init_values = {
        'from_date': filters.get('from_date'),
        'to_date': filters.get('to_date'),
    }
    filter_composer = make_filter_composer(
        filters, ['patient', 'sales_partner']
    )
    make_clauses = filter_composer(add_filter_clause)
    make_values = filter_composer(add_filter_value)
    return (
        " AND ".join(make_clauses(init_clauses)),
        make_values(init_values),
    )


def get_data(filters):
    clauses, values = make_conditions(filters)
    data = frappe.db.sql(
        """
            SELECT
                name AS sales_invoice,
                patient,
                posting_date,
                posting_time,
                total AS amount,
                discount_amount AS discount,
                grand_total AS total,
                paid_amount AS paid,
                outstanding_amount AS outstanding,
                total_commission AS commission,
                sales_partner
            FROM `tabSales Invoice`
            WHERE {clauses}
        """.format(clauses=clauses),
        values=values,
        as_dict=1,
    )
    sumby = compose(
        partial(reduce, add),
        partial(pluck, seqs=data),
    )
    return data + [{
        'sales_invoice': 'Total',
        'amount': sumby('amount'),
        'discount': sumby('discount'),
        'total': sumby('total'),
        'paid': sumby('paid'),
        'outstanding': sumby('outstanding'),
        'commission': sumby('commission'),
    }]


def make_row(row):
    posting_datetime = datetime.combine(
        row.get('posting_date'), datetime.min.time()
    ) + row.get('posting_time') if row.get('posting_date') else ''
    set_datetime = partial(
        assoc, key='posting_datetime', value=posting_datetime
    )
    keys = [
        'sales_invoice', 'patient', 'posting_datetime',
        'amount', 'discount', 'total',
        'paid', 'outstanding',
        'commission', 'sales_partner',
    ]
    return compose(
        partial(get, keys, default=''),
        set_datetime,
    )(row)
