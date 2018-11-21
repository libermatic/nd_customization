// Copyright (c) 2018, Libermatic and contributors
// For license information, please see license.txt

export const patient = {
  setup: function(frm) {
    frm.age_in_years = frappe.ui.form.make_control({
      parent: frm.fields_dict['age_in_years'].$wrapper,
      df: {
        fieldtype: 'Int',
        fieldname: 'age',
        label: 'Age',
      },
    });
  },
  refresh: function(frm) {
    frm.toggle_display('age_in_years', frm.doc.__islocal);
    if (frm.doc.__islocal) {
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
    }
  },
};

export default { patient };
