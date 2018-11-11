// Copyright (c) 2018, Libermatic and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sales Invoice', {
  patient: async function(frm) {
    const { patient } = frm.doc;
    if (patient) {
      const { message: doc = {} } = await frappe.db.get_value(
        'Patient',
        patient,
        'customer'
      );
      frm.set_value('customer', doc['customer']);
    } else {
      frm.set_value('patient_name', null);
      frm.set_value('customer', null);
    }
  },
});
