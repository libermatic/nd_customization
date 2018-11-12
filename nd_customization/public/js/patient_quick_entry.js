// Copyright (c) 2018, Libermatic and contributors
// For license information, please see license.txt

frappe.ui.form.PatientQuickEntryForm = frappe.ui.form.QuickEntryForm.extend({
  init: function(doctype, after_insert) {
    this._super(doctype, after_insert);
  },
  render_dialog: function() {
    this.mandatory = this.mandatory.concat(this.get_variant_fields());
    this._super();
  },
  insert: function() {
    if (this.dialog && this.dialog.doc) {
      const { age_in_years, dob } = this.dialog.doc;
      if (age_in_years && !dob) {
        this.dialog.doc.dob = frappe.datetime.obj_to_str(
          moment(frappe.datetime.year_start()).subtract(age_in_years, 'years')
        );
        this._super();
      }
    }
  },
  get_variant_fields: function() {
    return [
      {
        fieldtype: 'Section Break',
      },
      {
        label: 'Age in Years',
        fieldname: 'age_in_years',
        fieldtype: 'Int',
      },
      {
        fieldtype: 'Column Break',
      },
      {
        label: 'Date of Birth',
        fieldname: 'dob',
        fieldtype: 'Date',
      },
      {
        fieldtype: 'Section Break',
        label: __('Contact Details'),
        collapsible: 1,
      },
      {
        label: 'Mobile',
        fieldname: 'mobile',
        fieldtype: 'Data',
      },
      {
        label: 'Email',
        fieldname: 'email',
        fieldtype: 'Data',
        options: 'Email',
      },
      {
        fieldtype: 'Column Break',
      },
      {
        label: 'Address',
        fieldname: 'address_line1',
        fieldtype: 'Data',
      },
    ];
  },
});
