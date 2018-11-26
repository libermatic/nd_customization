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
    if doc.template and not doc.test_comment:
        template = frappe.get_doc('Lab Test Template', doc.template)
        if template and template.test_name != template.test_description:
            frappe.db.set_value(
                'Lab Test', doc.name, 'test_comment', template.test_description
            )
            doc.reload()


def before_cancel(doc, method):
    doc.flags.ignore_links = True


# this is necessary because allow_on_submit for status cannot be set for
# standard fields
def on_update_after_submit(doc, method):
    if doc.workflow_state in ['Approved', 'Rejected']:
        update_status(doc.workflow_state, doc.name)
        doc.reload()
