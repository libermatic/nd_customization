# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
from frappe.utils import flt, fmt_money
from erpnext.healthcare.doctype.lab_test.lab_test \
    import load_result_format


def validate(doc, method):
    if doc.additional_discount_percentage or doc.discount_amount:
        for item in doc.items:
            max_discount = frappe.db.get_value(
                'Item', item.item_code, 'max_discount'
            )
            discount = (1.0 - flt(item.net_rate) / flt(item.price_list_rate)) \
                * 100.0
            if max_discount and discount > flt(max_discount):
                min_price = flt(item.price_list_rate) * \
                    (1.0 - max_discount / 100.0)
                frappe.throw(
                    'Maximum discount for Item {0} is {1}%. Net Rate cannot '
                    'be less than {2}'.format(
                        item.item_code,
                        max_discount,
                        fmt_money(min_price, currency=doc.currency),
                    )
                )


def on_submit(doc, method):
    if doc.patient:
        lab_tests = []
        patient = frappe.get_doc('Patient', doc.patient)
        for item in doc.items:
            if item.reference_dt == 'Lab Test':
                test = frappe.get_doc('Lab Test', item.reference_dn)
                if test and not test.invoice:
                    test.invoice = doc.name
                    test.save(ignore_permissions=True)
                    lab_tests.append(item.reference_dn)
            else:
                template = _get_lab_test_template(item.item_code)
                if template:
                    test = _make_lab_test(
                        patient, template, doc, item.lab_test_result_date
                    )
                    test.insert(ignore_permissions=True)
                    load_result_format(test, template, None, None)
                    frappe.db.set_value(
                        'Sales Invoice Item',
                        item.name,
                        'reference_dt',
                        'Lab Test',
                    )
                    frappe.db.set_value(
                        'Sales Invoice Item',
                        item.name,
                        'reference_dn',
                        test.name,
                    )
                    lab_tests.append(test.name)
        if lab_tests:
            frappe.msgprint(
                'Lab Test(s) {} linked.'.format(', '.join(lab_tests))
            )
        else:
            frappe.msgprint('No Lab Test created.')
        doc.reload()


def on_cancel(doc, method):
    if doc.patient:
        lab_tests = []
        for item in doc.items:
            if item.reference_dt == 'Lab Test' and item.reference_dn:
                test = frappe.get_doc('Lab Test', item.reference_dn)
                if test.docstatus < 1:
                    test.invoice = None
                    test.save(ignore_permissions=True)
                    lab_tests.append(item.reference_dn)
        if lab_tests:
            frappe.msgprint(
                'Lab Test(s) {} unlinked from Sales Invoice.'.format(
                    ', '.join(lab_tests)
                )
            )


def _get_lab_test_template(item):
    template = frappe.db.exists('Lab Test Template', {'item': item})
    return frappe.get_doc("Lab Test Template", template) if template else None


def _make_lab_test(patient, template, invoice, result_date):
    return frappe.get_doc({
        'doctype': 'Lab Test',
        'invoice': invoice.name,
        'patient': patient.name,
        'patient_name': patient.patient_name,
        'patient_age': patient.get_age(),
        'patient_sex': patient.sex,
        'doctor': invoice.ref_physician,
        'email': patient.email,
        'mobile': patient.mobile,
        'company': invoice.company,
        'department': template.department,
        'report_preference': patient.report_preference,
        'test_name': template.test_name,
        'template': template.name,
        'result_date': result_date,
    })
