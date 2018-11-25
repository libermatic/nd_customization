// Copyright (c) 2018, Libermatic and contributors
// For license information, please see license.txt

export const lab_test_template = {
  refresh: async function(frm) {
    if (frm.doc.__islocal) {
      const { message: settings } = await frappe.db.get_value(
        'Healthcare Settings',
        null,
        'templates_use_naming_series'
      );
      if (parseInt(settings.templates_use_naming_series)) {
        frm.set_df_property('test_code', 'hidden', 1);
        frm.set_df_property('test_code', 'reqd', 0);
      }
    }
  },
};

export default { lab_test_template };
