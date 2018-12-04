# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
from frappe.utils import cint
from frappe.model.naming import get_default_naming_series, make_autoname


def autoname(doc, method):
    uses_naming_series = frappe.db.get_value(
        'Healthcare Settings', None, 'templates_use_naming_series',
    )
    if cint(uses_naming_series):
        key = get_default_naming_series('Lab Test Template')
        doc.test_code = make_autoname(key, 'Lab Test Template', doc)


def after_insert(doc, method):
    if doc.item:
        _set_purchase_flag(doc)


def on_update(doc, method):
    if doc.item:
        _set_purchase_flag(doc)


def _set_purchase_flag(doc):
    frappe.db.set_value(
        'Item', doc.item, 'is_purchase_item', doc.can_outsource
    )
    doc.reload()
