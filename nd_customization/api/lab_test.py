# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
import json
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
    if template.test_template_type == 'Compound':
        subsections = _get_subsections(template.normal_test_templates)
        if subsections:
            for item in doc.normal_test_items:
                if item.test_name in subsections:
                    frappe.db.set_value(
                        'Normal Test Items',
                        item.name,
                        'require_result_value',
                        0,
                    )
                elif item.test_name and not item.test_event:
                    frappe.db.set_value(
                        'Normal Test Items',
                        item.name,
                        'test_name',
                        None,
                    )
                    frappe.db.set_value(
                        'Normal Test Items',
                        item.name,
                        'test_event',
                        item.test_name,
                    )
    if template.test_template_type == 'Grouped':
        for item in doc.normal_test_items:
            if item.test_name and item.template \
                    and item.template != doc.template:
                test_comment = frappe.db.get_value(
                    'Lab Test Template', item.template, 'test_comment'
                )
                if test_comment:
                    frappe.db.set_value(
                        'Normal Test Items',
                        item.name,
                        'test_comment',
                        test_comment,
                    )


def load_result_format(lab_test, template, prescription, invoice):
    from erpnext.healthcare.doctype.lab_test.lab_test \
        import load_result_format
    load_result_format(lab_test, template, prescription, invoice)
    change_test_loading(lab_test, template)


@frappe.whitelist()
def create_invoice(company, patient, lab_tests, prescriptions):
    from erpnext.healthcare.doctype.lab_test.lab_test import create_invoice
    si_name = create_invoice(company, patient, lab_tests, prescriptions)
    test_ids = json.loads(lab_tests)
    if test_ids:
        si = frappe.get_doc('Sales Invoice', si_name)
        si.patient = patient
        find_item = _find_item(si.items)
        for test_id in test_ids:
            test = frappe.get_doc('Lab Test', test_id)
            item_code = frappe.db.get_value(
                'Lab Test Template', test.template, 'item'
            )
            item = find_item(item_code)
            item.reference_dt = 'Lab Test'
            item.reference_dn = test_id
            item.lab_test_result_date = test.result_date
        si.save()
    return si_name


def _find_item(items):
    def fn(item_code):
        for item in items:
            if item.item_code == item_code:
                return item
    return fn


@frappe.whitelist()
def link_invoice(lab_test, sales_invoice):
    test_doc = frappe.get_doc('Lab Test', lab_test)
    invoice_doc = frappe.get_doc('Sales Invoice', sales_invoice)
    if test_doc.docstatus == 2 or invoice_doc.docstatus == 2:
        frappe.throw('Cannot link cancelled documents.')
    if test_doc.patient != invoice_doc.patient:
        frappe.throw(
            'Lab Test and Sales Invoice belong to different Patients.'
        )
    frappe.db.set_value('Lab Test', lab_test, 'invoice', sales_invoice)
