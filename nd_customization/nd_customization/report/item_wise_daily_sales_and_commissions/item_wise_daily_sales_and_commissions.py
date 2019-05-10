# Copyright (c) 2013, Libermatic and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from datetime import datetime
from functools import partial
from toolz import compose, pluck, keyfilter, merge


def execute(filters=None):
    columns, data = _get_columns(), _get_data(filters)
    return columns, map(_pick_fields(columns), data)


def _pick_fields(columns):
    keys = compose(list, partial(pluck, "fieldname"))(columns)
    return partial(keyfilter, lambda k: k in keys)


def _get_columns():
    return [
        {
            "label": _("Sales Invoice"),
            "fieldname": "sales_invoice",
            "fieldtype": "Link",
            "options": "Sales Invoice",
            "width": 120,
        },
        {
            "label": _("Patient ID"),
            "fieldname": "patient",
            "fieldtype": "Link",
            "options": "Patient",
            "width": 90,
        },
        {
            "label": _("Patient Name"),
            "fieldname": "patient_name",
            "fieldtype": "Data",
            "width": 120,
        },
        {
            "label": _("Test Code"),
            "fieldname": "test_code",
            "fieldtype": "Link",
            "options": "Lab Test Template",
            "width": 90,
        },
        {
            "label": _("Test Name"),
            "fieldname": "test_name",
            "fieldtype": "Data",
            "width": 120,
        },
        {
            "label": _("Time"),
            "fieldname": "posting_datetime",
            "fieldtype": "Datetime",
            "width": 150,
        },
        {
            "label": _("Amount"),
            "fieldname": "amount",
            "fieldtype": "Currency",
            "width": 90,
        },
        {
            "label": _("Net Amount"),
            "fieldname": "net_amount",
            "fieldtype": "Currency",
            "width": 90,
        },
        {
            "label": _("Referring Physician"),
            "fieldname": "physician",
            "fieldtype": "Link",
            "options": "Physician",
            "width": 120,
        },
        {
            "label": _("Sales Partner"),
            "fieldname": "sales_partner",
            "fieldtype": "Link",
            "options": "Sales Partner",
            "width": 120,
        },
    ]


def _get_data(filters):
    data = frappe.db.sql(
        """
            SELECT
                sii.item_code AS test_code,
                sii.item_name AS test_name,
                si.name AS sales_invoice,
                si.patient AS patient,
                si.patient_name AS patient_name,
                si.posting_date AS posting_date,
                si.posting_time AS posting_time,
                sii.amount AS amount,
                sii.net_amount AS net_amount,
                si.ref_physician AS physician,
                si.sales_partner AS sales_partner
            FROM `tabSales Invoice Item` as sii
            LEFT JOIN `tabSales Invoice` AS si ON si.name = sii.parent
            WHERE {clauses}
        """.format(
            clauses=_get_clauses(filters)
        ),
        as_dict=1,
        values=filters,
    )

    def set_datetime(item):
        return merge(
            item,
            {
                "posting_datetime": (
                    datetime.combine(item.get("posting_date"), datetime.min.time())
                    + item.get("posting_time")
                    if item.get("posting_date")
                    else ""
                )
            },
        )

    return map(set_datetime, data)


def _get_clauses(filters):
    conditions = [
        "si.docstatus = 1",
        "posting_date BETWEEN %(from_date)s AND %(to_date)s",
    ]
    if filters.get("patient"):
        conditions += ["si.patient = %(patient)s"]
    if filters.get("physician"):
        conditions += ["si.ref_physician = %(physician)s"]
    if filters.get("sales_partner"):
        conditions += ["si.sales_partner = %(sales_partner)s"]
    return " AND ".join(conditions)
