// Copyright (c) 2018, Libermatic and contributors
// For license information, please see license.txt

frappe.ui.form.on('Patient', {
  setup: function(frm) {
    frm.age_in_years = frappe.ui.form.make_control({
      parent: frm.fields_dict['age_in_years'].$wrapper,
      df: {
        fieldtype: 'Int',
        fieldname: 'age',
        label: 'Age',
      },
    });
    console.log(frm.age_in_years);
  },
  refresh: function(frm) {
    frm.age_in_years.refresh();
    frm.age_in_years.$input.change(function() {
      const age = frm.age_in_years.get_value();
      frm.set_value(
        'dob',
        frappe.datetime.obj_to_str(
          moment(frappe.datetime.year_start()).subtract(age, 'years')
        )
      );
    });
  },
});
