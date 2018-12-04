# -*- coding: utf-8 -*-
# Copyright (c) 2018, Libermatic and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class LabTestCenter(Document):
    def after_insert(self):
        create_supplier(self)
        self.reload()


def create_supplier(doc):
    supplier_type = frappe.db.get_value(
        'Buying Settings', None, 'supplier_type'
    )
    if not supplier_type:
        frappe.throw(
            'Please set <em>Default Supplier Type</em> in Buying Settings.'
        )
    supplier = frappe.get_doc({
        'doctype': 'Supplier',
        'supplier_name': doc.test_center,
        'supplier_type': supplier_type,
    }).insert(ignore_permissions=True)
    frappe.db.set_value('Lab Test Center', doc.name, 'supplier', supplier.name)
    frappe.msgprint(
        'Supplier {0} is created.'.format(supplier.name),
        alert=True,
    )
