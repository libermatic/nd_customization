# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
from erpnext.healthcare.doctype.lab_test.lab_test import update_status


def validate(doc, method):
    if not doc.is_new():
        before = doc.get_doc_before_save()
        if before.workflow_state == 'Discarded':
            frappe.throw('Cannot save a Discarded Lab Test. Create a new one.')


def after_insert(doc, method):
    if doc.template:
        template = frappe.get_doc('Lab Test Template', doc.template)
        if template and not doc.test_comment and template.test_comment:
            frappe.db.set_value(
                'Lab Test',
                doc.name,
                'test_comment',
                template.test_comment,
            )
        if template and not doc.custom_result and template.test_custom_result:
            frappe.db.set_value(
                'Lab Test',
                doc.name,
                'custom_result',
                template.test_custom_result,
            )
        if template and doc.sample and template.sample_in_print:
            frappe.db.set_value(
                'Lab Test',
                doc.name,
                'sample_in_print',
                template.sample_in_print,
            )
        if template.test_template_type == 'No Result' and not doc.test_name:
            update = {
                'test_name': template.test_name,
                'department': template.department,
                'test_group': template.test_group,
            }
            for k, v in update.iteritems():
                frappe.db.set_value('Lab Test', doc.name, k, v)
        doc.reload()


def before_cancel(doc, method):
    doc.flags.ignore_links = True


# this is necessary because allow_on_submit for status cannot be set for
# standard fields
def on_update_after_submit(doc, method):
    if doc.workflow_state in ['Approved', 'Rejected']:
        update_status(doc.workflow_state, doc.name)
        doc.reload()
