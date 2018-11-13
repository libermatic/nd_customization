# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe


def before_submit(doc, method):
    if not doc.employee:
        doc.employee = frappe.db.exists(
            'Employee', {'user_id': frappe.session.user},
        )
        if doc.employee:
            doc.employee_name = frappe.db.get_value(
                'Employee', doc.employee, 'employee_name',
            )
