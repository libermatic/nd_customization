// Copyright (c) 2018, Libermatic and contributors
// For license information, please see license.txt

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

export const lab_test = {
  refresh: function(frm) {
    render_dashboard(frm);
  },
  employee: function(frm) {
    if (!frm.doc['employee']) {
      frm.set_value('employee_name', null);
    }
  },
};

export default { lab_test };
