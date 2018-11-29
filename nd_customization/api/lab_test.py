# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
from frappe.utils import now, cint


@frappe.whitelist()
def deliver_result(lab_test, revert=0, delivery_time=None):
    doc = frappe.get_doc('Lab Test', lab_test)
    if doc and doc.docstatus == 1:
        if cint(revert):
            doc.delivery_time = None
        else:
            doc.delivery_time = delivery_time or now()
        doc.save()
