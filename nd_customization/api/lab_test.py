# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
from frappe.utils import now, cint
from functools import partial
from toolz import compose


@frappe.whitelist()
def deliver_result(lab_test, revert=0, delivery_time=None):
    doc = frappe.get_doc('Lab Test', lab_test)
    if doc and doc.docstatus == 1:
        if cint(revert):
            doc.delivery_time = None
        else:
            doc.delivery_time = delivery_time or now()
        doc.save()


_get_subsections = compose(
    partial(map, lambda x: x.test_event),
    partial(filter, lambda x: cint(x.is_subsection) == 1)
)


def change_test_loading(doc, template):
    subsections = _get_subsections(template.normal_test_templates)
    if subsections:
        normal_tests_items = frappe.get_all(
            'Normal Test Items',
            fields=['name', 'test_name', 'test_event'],
            filters={
                'parent': doc.name,
                'parentfield': 'normal_test_items',
            }
        )
        for item in normal_tests_items:
            if item.get('test_name') in subsections:
                frappe.db.set_value(
                    'Normal Test Items',
                    item.get('name'),
                    'require_result_value',
                    0,
                )
            elif item.get('test_name') and not item.get('test_event'):
                frappe.db.set_value(
                    'Normal Test Items',
                    item.get('name'),
                    'test_name',
                    None,
                )
                frappe.db.set_value(
                    'Normal Test Items',
                    item.get('name'),
                    'test_event',
                    item.get('test_name'),
                )
