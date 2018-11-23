// Copyright (c) 2018, Libermatic and contributors
// For license information, please see license.txt

import { omit } from '../utils';

async function render_dashboard(frm) {
  if (!!frm.doc['invoice']) {
    function get_color(status) {
      switch (status) {
        case 'Paid':
          return 'green';
        case 'Overdue':
          return 'red';
        case 'Unpaid':
          return 'orange';
        default:
          return 'darkgrey';
      }
    }
    const { message: si } = await frappe.db.get_value(
      'Sales Invoice',
      frm.doc['invoice'],
      'status'
    );
    frm.dashboard.add_indicator(`Invoice - ${si.status}`, get_color(si.status));
    frm.dashboard.show();
  }
}

function add_menus_items(frm) {
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

export const lab_test = {
  refresh: function(frm) {
    render_dashboard(frm);
    add_menus_items(frm);
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
};

export default { lab_test };
