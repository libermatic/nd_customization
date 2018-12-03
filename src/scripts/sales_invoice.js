// Copyright (c) 2018, Libermatic and contributors
// For license information, please see license.txt

export const sales_invoice = {
  onload: function(frm) {
    if (frm.doc.docstatus === 1) {
      frm.add_custom_button(
        'Lab Test',
        () => frappe.set_route('List', 'Lab Test', { invoice: frm.doc.name }),
        __('View')
      );
    }
  },
  patient: async function(frm) {
    const { patient } = frm.doc;
    if (patient) {
      const { message: doc = {} } = await frappe.db.get_value(
        'Patient',
        patient,
        'customer'
      );
      frm.set_value('customer', doc['customer']);
      frm.set_value('is_pos', 1);
    } else {
      frm.set_value('patient_name', null);
      frm.set_value('customer', null);
      frm.set_value('is_pos', 0);
    }
  },
};

export default { sales_invoice };
