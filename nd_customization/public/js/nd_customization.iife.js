var nd_customization = (function () {
  'use strict';

  // Copyright (c) 2018, Libermatic and contributors
  // For license information, please see license.txt
  const patient = {
    setup: function (frm) {
      frm.age_in_years = frappe.ui.form.make_control({
        parent: frm.fields_dict['age_in_years'].$wrapper,
        df: {
          fieldtype: 'Int',
          fieldname: 'age',
          label: 'Age'
        }
      });
    },
    refresh: function (frm) {
      frm.toggle_display('age_in_years', frm.doc.__islocal);

      if (frm.doc.__islocal) {
        frm.age_in_years.refresh();
        frm.age_in_years.$input.change(function () {
          const age = frm.age_in_years.get_value();
          frm.set_value('dob', frappe.datetime.obj_to_str(moment(frappe.datetime.year_start()).subtract(age, 'years')));
        });
      }
    }
  };

  function omit(keys, object) {
    function reducer_fn(acc, key) {
      if (!keys.includes(key)) {
        return Object.assign(acc, {
          [key]: object[key]
        });
      }

      return acc;
    }

    return Object.keys(object).reduce(reducer_fn, {});
  }

  // Copyright (c) 2018, Libermatic and contributors

  async function render_dashboard(frm) {
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

      const {
        message: si
      } = await frappe.db.get_value('Sales Invoice', frm.doc['invoice'], 'status');
      frm.dashboard.add_indicator(`Invoice - ${si.status}`, get_color(si.status));
      frm.dashboard.show();
    }
  }

  function add_menus_items(frm) {
    if (['Discarded', 'Rejected'].includes(frm.doc.workflow_state)) {
      frm.page.add_menu_item('Clone Test', async function () {
        const {
          doc
        } = frm;
        const cloned = frappe.model.copy_doc(omit(['email_sent', 'patient_age', 'printed', 'sms_sent', 'status'], doc), doc.name);
        frappe.set_route('Form', cloned.doctype, cloned.name);
      });
    }
  }

  const lab_test = {
    refresh: function (frm) {
      render_dashboard(frm);
      add_menus_items(frm);

      if (frm.doc.docstatus === 0 && frm.doc.workflow_state === 'Discarded') {
        frm.fields.map(({
          df
        }) => df.fieldname).filter(field => field).forEach(field => frm.set_df_property(field, 'read_only', 1));
      }
    },
    employee: function (frm) {
      if (!frm.doc['employee']) {
        frm.set_value('employee_name', null);
      }
    }
  };

  // Copyright (c) 2018, Libermatic and contributors
  // For license information, please see license.txt
  const sales_invoice = {
    patient: async function (frm) {
      const {
        patient
      } = frm.doc;

      if (patient) {
        const {
          message: doc = {}
        } = await frappe.db.get_value('Patient', patient, 'customer');
        frm.set_value('customer', doc['customer']);
        frm.set_value('is_pos', 1);
      } else {
        frm.set_value('patient_name', null);
        frm.set_value('customer', null);
        frm.set_value('is_pos', 0);
      }
    }
  };

  var scripts = {
    patient,
    lab_test,
    sales_invoice
  };

  var index$1 = {
    scripts
  };

  return index$1;

}());
