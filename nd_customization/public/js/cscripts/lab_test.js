// Copyright (c) 2018, Libermatic and contributors
// For license information, please see license.txt

frappe.ui.form.on('Lab Test', {
  refresh: function(frm) {
    frm.trigger('render_dashboard');
  },
  employee: function(frm) {
    if (!frm.doc['employee']) {
      frm.set_value('employee_name', null);
    }
  },
  render_dashboard: async function(frm) {
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
      frm.dashboard.add_indicator(
        `Invoice - ${si.status}`,
        get_color(si.status)
      );
      frm.dashboard.show();
    }
  },
});
