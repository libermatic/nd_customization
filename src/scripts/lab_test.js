// Copyright (c) 2018, Libermatic and contributors
// For license information, please see license.txt

import { omit } from '../utils';

function get_color(status) {
  if (status === 'Pending') {
    return 'blue';
  }
  if (['Unpaid', 'Completed', 'Not Collected'].includes(status)) {
    return 'orange';
  }
  if (['Paid', 'Collected', 'Approved'].includes(status)) {
    return 'green';
  }
  if (['Overdue', 'Rejected'].includes(status)) {
    return 'red';
  }
  return 'darkgrey';
}

async function render_dashboard(frm) {
  const dashboard_indicators = [];
  if (!!frm.doc['invoice']) {
    const { message: si } = await frappe.db.get_value(
      'Sales Invoice',
      frm.doc['invoice'],
      'status'
    );
    dashboard_indicators.push([`Invoice - ${si.status}`, get_color(si.status)]);
  }
  if (!!frm.doc['sample']) {
    const { message: sc } = await frappe.db.get_value(
      'Sample Collection',
      frm.doc['sample'],
      'docstatus'
    );
    const status = sc.docstatus ? 'Collected' : 'Not Collected';
    dashboard_indicators.push([`Sample - ${status}`, get_color(status)]);
  }
  if (dashboard_indicators.length > 0) {
    dashboard_indicators.forEach(([label, color]) =>
      frm.dashboard.add_indicator(label, color)
    );
    frm.dashboard.show();
  }
}

function render_clone_action(frm) {
  if (['Discarded', 'Rejected'].includes(frm.doc.workflow_state)) {
    frm.page.add_menu_item('Clone Test', async function() {
      const { doc } = frm;
      const cloned = frappe.model.copy_doc(
        omit(
          ['email_sent', 'patient_age', 'printed', 'sms_sent', 'status'],
          doc
        ),
        doc.name
      );
      frappe.set_route('Form', cloned.doctype, cloned.name);
    });
  }
}

function render_delivery_actions(frm) {
  if (frm.doc.docstatus === 1) {
    const is_delivered = !!frm.doc.delivery_time;
    frm
      .add_custom_button('Mark Delivered', async function() {
        await frappe.call({
          method: 'nd_customization.api.lab_test.deliver_result',
          args: { lab_test: frm.doc.name },
        });
        frm.reload_doc();
      })
      .toggleClass('disabled', is_delivered);
    if (is_delivered) {
      frm.page.add_menu_item('Mark Undelivered', async function() {
        await frappe.call({
          method: 'nd_customization.api.lab_test.deliver_result',
          args: { lab_test: frm.doc.name, revert: 1 },
        });
        frm.reload_doc();
      });
    }
  }
}

export const lab_test = {
  refresh: function(frm) {
    render_dashboard(frm);
    render_clone_action(frm);
    render_delivery_actions(frm);
    if (frm.doc.docstatus === 0 && frm.doc.workflow_state === 'Discarded') {
      frm.fields
        .map(({ df }) => df.fieldname)
        .filter(field => field)
        .forEach(field => frm.set_df_property(field, 'read_only', 1));
    }
  },
  employee: function(frm) {
    if (!frm.doc['employee']) {
      frm.set_value('employee_name', null);
    }
  },
  on_submit: function(frm) {
    frm.reload_doc();
  },
};

export default { lab_test };
