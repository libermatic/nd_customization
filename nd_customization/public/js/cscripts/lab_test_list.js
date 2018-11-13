// Copyright (c) 2018, Libermatic and contributors
// For license information, please see license.txt

frappe.listview_settings['Lab Test'] = {
  add_fields: ['status', 'email_sent', 'printed', 'invoice'],
  filters: [['docstatus', '=', '0']],
  get_indicator: function({ status, email_sent, printed, invoice }) {
    function get_color(status) {
      switch (status) {
        case 'Completed':
          return 'blue';
        case 'Approved':
          return 'green';
        case 'Rejected':
          return 'yellow';
        default:
          return 'darkgrey';
      }
    }
    return [status, get_color(status), `status,=,${status}`];
  },
};
