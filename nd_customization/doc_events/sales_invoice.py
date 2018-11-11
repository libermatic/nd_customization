# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe


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
                    test = _make_lab_test(patient, template, doc)
                    test.insert(ignore_permissions=True)
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


def _make_lab_test(patient, template, invoice):
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
    })
