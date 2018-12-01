# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe


def execute():
    if not frappe.db.exists('Party Type', 'Sales Partner'):
        frappe.get_doc({
            'doctype': 'Party Type',
            'party_type': 'Sales Partner',
        }).insert(ignore_permissions=True)
