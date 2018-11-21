# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from erpnext.healthcare.doctype.lab_test.lab_test import update_status


def before_cancel(doc, method):
    doc.flags.ignore_links = True


# this is necessary because allow_on_submit for status cannot be set for
# standard fields
def on_update_after_submit(doc, method):
    if doc.workflow_state in ['Approved', 'Rejected']:
        update_status(doc.workflow_state, doc.name)
