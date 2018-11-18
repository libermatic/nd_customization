# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# included here because this file has not been comitted to master

from __future__ import unicode_literals
import frappe
from frappe.utils import cint
from frappe import _


class WorkflowStateError(frappe.ValidationError):
    pass


class WorkflowTransitionError(frappe.ValidationError):
    pass


class WorkflowPermissionError(frappe.ValidationError):
    pass


def get_workflow_name(doctype):
    workflow_name = frappe.cache().hget('workflow', doctype)
    if workflow_name is None:
        workflow_name = frappe.db.get_value(
            'Workflow', {'document_type': doctype, 'is_active': 1}, 'name')
        frappe.cache().hset('workflow', doctype, workflow_name or '')
    return workflow_name


def get_transitions(doc, workflow=None):
    '''Return list of possible transitions for the given doc'''

    if doc.is_new():
        return []

    frappe.has_permission(doc=doc, ptype='read', throw=True)
    roles = frappe.get_roles()

    if not workflow:
        workflow = get_workflow(doc.doctype)
    current_state = doc.get(workflow.workflow_state_field)

    if not current_state:
        frappe.throw(_('Workflow State not set'), WorkflowStateError)

    transitions = []
    for transition in workflow.transitions:
        if transition.state == current_state and transition.allowed in roles:
            if transition.get('condition'):
                # if condition, evaluate
                # access to frappe.db.get_value and frappe.db.get_list
                success = frappe.safe_eval(
                    transition.condition,
                    dict(
                        frappe=frappe._dict(
                            db=frappe._dict(
                                get_value=frappe.db.get_value,
                                get_list=frappe.db.get_list,
                            ),
                            session=frappe.session,
                        )
                    ),
                    dict(doc=doc),
                )
                if not success:
                    continue
            transitions.append(transition.as_dict())

    return transitions


def apply_workflow(doc, action):
    '''Allow workflow action on the current doc'''
    workflow = get_workflow(doc.doctype)
    transitions = get_transitions(doc, workflow)

    # find the transition
    transition = None
    for t in transitions:
        if t.action == action:
            transition = t

    if not transition:
        frappe.throw(_("Not a valid Workflow Action"), WorkflowTransitionError)

    # update workflow state field
    doc.set(workflow.workflow_state_field, transition.next_state)

    # find settings for the next state
    next_state = [
        d for d in workflow.states if d.state == transition.next_state
    ][0]

    # update any additional field
    if next_state.update_field:
        doc.set(next_state.update_field, next_state.update_value)

    new_docstatus = cint(next_state.doc_status)
    if doc.docstatus == 0 and new_docstatus == 0:
        doc.save()
    elif doc.docstatus == 0 and new_docstatus == 1:
        doc.submit()
    elif doc.docstatus == 1 and new_docstatus == 1:
        doc.save()
    elif doc.docstatus == 1 and new_docstatus == 2:
        doc.cancel()
    else:
        frappe.throw(
            _('Illegal Document Status for {0}').format(next_state.state)
        )

    doc.add_comment('Workflow', _(next_state.state))

    return doc


def get_workflow(doctype):
    return frappe.get_doc('Workflow', get_workflow_name(doctype))
