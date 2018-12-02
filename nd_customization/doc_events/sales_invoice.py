# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
from frappe.utils import flt, fmt_money
from erpnext.healthcare.doctype.lab_test.lab_test \
    import create_sample_collection, load_result_format
from erpnext.accounts.doctype.sales_invoice.sales_invoice \
    import get_bank_cash_account
from toolz import pluck

from nd_customization.api.workflow import apply_workflow
from nd_customization.api.lab_test import change_test_loading


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
            test = frappe.get_doc('Lab Test', item.reference_dn) \
                if item.reference_dt and item.reference_dn else None
            if test and test.status != 'Cancelled' and not test.invoice:
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
                    create_sample_collection(test, template, patient, doc.name)
                    load_result_format(test, template, None, doc.name)
                    change_test_loading(test, template)
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
                'Lab Test(s) {} created.'.format(', '.join(lab_tests))
            )
        else:
            frappe.msgprint('No Lab Test created.')
        doc.reload()
    if doc.sales_partner:
        settings = frappe.get_single('ND Settings')
        je = _make_journal_entry(doc, frappe._dict({
            'voucher_type':
                'Cash Entry' if settings.sales_partner_mop == 'Cash' else
                'Bank Entry',
            'accounts': [
                frappe._dict({
                    'account': settings.sales_partner_ca,
                    'cost_center': settings.sales_partner_cc,
                    'party_type': 'Sales Partner',
                    'party': doc.sales_partner,
                    'debit': 0,
                }),
                frappe._dict({
                    'account': get_bank_cash_account(
                        settings.sales_partner_mop, doc.company
                    ).get('account'),
                    'credit': 0,
                }),
            ],
            'user_remark': _get_je_remark(doc),
            'pay_to_recd_from': doc.sales_partner,
        }))
        je.insert(ignore_permissions=True)


def on_cancel(doc, method):
    if doc.sales_partner:
        jes = frappe.get_all(
            'Journal Entry',
            filters={
                'docstatus': 0,
                'reference_dt': doc.doctype,
                'reference_dn': doc.name,
            }
        )
        for name in pluck('name', jes):
            frappe.delete_doc('Journal Entry', name)
    if doc.patient:
        lab_tests = []
        for item in doc.items:
            if item.reference_dt == 'Lab Test' and item.reference_dn:
                test = frappe.get_doc('Lab Test', item.reference_dn)
                if test.docstatus < 1 and test.workflow_state == 'Pending':
                    test.flags.ignore_links = True
                    apply_workflow(test, 'Reject')
                    lab_tests.append(item.reference_dn)
        if lab_tests:
            frappe.msgprint(
                'Lab Test(s) {} discarded.'.format(', '.join(lab_tests))
            )
        doc.reload()


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
        'test_group': template.test_group,
        'report_preference': patient.report_preference,
        'test_name': template.test_name,
        'template': template.name,
        'result_date': result_date,
        'workflow_state': 'Pending',
    })


def _make_journal_entry(doc, args):
    je = frappe.get_doc({
        'doctype': 'Journal Entry',
        'voucher_type': args.voucher_type,
        'posting_date': doc.posting_date,
        'company': doc.company,
        'user_remark': args.user_remark,
        'pay_to_recd_from': args.pay_to_recd_from,
        'reference_dt': doc.doctype,
        'reference_dn': doc.name,
    })
    for account in args.accounts:
        je.append('accounts', account)
    return je


def _get_je_remark(doc):
    remark = '{}: {}\n'.format(doc.patient, doc.patient_name)
    for item in doc.items:
        remark += '/ {}: {}\n'.format(item.item_code, item.item_name)
    return remark
