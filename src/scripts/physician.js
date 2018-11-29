// Copyright (c) 2018, Libermatic and contributors
// For license information, please see license.txt

export const physician = {
  employee: function(frm) {
    if (frm.doc.__islocal) {
      ['employee', 'designation', 'first_name', 'mobile_phone'].forEach(field =>
        frm.set_value(field, null)
      );
    }
  },
};

export default { physician };
