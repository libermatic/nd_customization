// Copyright (c) 2018, Libermatic and contributors
// For license information, please see license.txt

frappe.ui.form.on('ND Settings', {
  refresh: function(frm) {
    frm.set_query('sales_partner_ca', { filters: { root_type: 'Expense' } });
  },
});
