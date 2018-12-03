var nd_customization = (function () {
  'use strict';

  // Copyright (c) 2018, Libermatic and contributors
  // For license information, please see license.txt
  const physician = {
    employee: function (frm) {
      if (frm.doc.__islocal) {
        ['employee', 'designation', 'first_name', 'mobile_phone'].forEach(field => frm.set_value(field, null));
      }
    }
  };

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

  // Copyright (c) 2018, Libermatic and contributors
  // For license information, please see license.txt
  const lab_test_template = {
    refresh: async function (frm) {
      if (frm.doc.__islocal) {
        const {
          message: settings
        } = await frappe.db.get_value('Healthcare Settings', null, 'templates_use_naming_series');

        if (parseInt(settings.templates_use_naming_series)) {
          frm.set_df_property('test_code', 'hidden', 1);
          frm.set_df_property('test_code', 'reqd', 0);
        }
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

  function get_color(status) {
    if (status === 'Pending') {
      return 'blue';
    }

    if (['Unpaid', 'Completed', 'Not Collected'].includes(status)) {
      return 'orange';
    }

    if (['Paid', 'Collected', 'Approved'].includes(status)) {
      return 'green';
    }

    if (['Overdue', 'Rejected'].includes(status)) {
      return 'red';
    }

    return 'darkgrey';
  }

  async function render_dashboard(frm) {
    const dashboard_indicators = [];

    if (!!frm.doc['invoice']) {
      const {
        message: si
      } = await frappe.db.get_value('Sales Invoice', frm.doc['invoice'], 'status');
      dashboard_indicators.push([`Invoice - ${si.status}`, get_color(si.status)]);
    }

    if (!!frm.doc['sample']) {
      const {
        message: sc
      } = await frappe.db.get_value('Sample Collection', frm.doc['sample'], 'docstatus');
      const status = sc.docstatus ? 'Collected' : 'Not Collected';
      dashboard_indicators.push([`Sample - ${status}`, get_color(status)]);
    }

    if (dashboard_indicators.length > 0) {
      dashboard_indicators.forEach(([label, color]) => frm.dashboard.add_indicator(label, color));
      frm.dashboard.show();
    }
  }

  function render_clone_action(frm) {
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

  function render_delivery_actions(frm) {
    if (frm.doc.docstatus === 1) {
      const is_delivered = !!frm.doc.delivery_time;
      frm.add_custom_button('Mark Delivered', async function () {
        await frappe.call({
          method: 'nd_customization.api.lab_test.deliver_result',
          args: {
            lab_test: frm.doc.name
          }
        });
        frm.reload_doc();
      }).toggleClass('disabled', is_delivered);

      if (is_delivered) {
        frm.page.add_menu_item('Mark Undelivered', async function () {
          await frappe.call({
            method: 'nd_customization.api.lab_test.deliver_result',
            args: {
              lab_test: frm.doc.name,
              revert: 1
            }
          });
          frm.reload_doc();
        });
      }
    }
  }

  function render_invoice_actions(frm) {
    if (!frm.doc.__islocal && frm.doc.docstatus < 2) {
      if (!frm.doc.invoice) {
        const dialog = new frappe.ui.Dialog({
          title: 'Select Sales Invoice',
          fields: [{
            fieldname: 'sales_invoice',
            fieldtype: 'Link',
            options: 'Sales Invoice',
            label: 'Sales Invoice',
            get_query: {
              filters: {
                patient: frm.doc.patient
              }
            }
          }],
          primary_action: async function () {
            const sales_invoice = this.get_value('sales_invoice');
            await frappe.call({
              method: 'nd_customization.api.lab_test.link_invoice',
              args: {
                lab_test: frm.doc.name,
                sales_invoice
              },
              freeze: true,
              freeze_message: `Linking Sales Invoice: ${sales_invoice}`
            });
            this.hide();
            frm.reload_doc();
          }
        });
        frm.add_custom_button('Link Invoice', () => {
          dialog.show();
        });
      }
    }
  }

  const lab_test = {
    onload: function (frm) {
      render_dashboard(frm);
      render_clone_action(frm);
      render_delivery_actions(frm);
    },
    refresh: function (frm) {
      render_invoice_actions(frm);

      if (frm.doc.docstatus === 0 && frm.doc.workflow_state === 'Discarded') {
        frm.fields.map(({
          df
        }) => df.fieldname).filter(field => field).forEach(field => frm.set_df_property(field, 'read_only', 1));
      }

      frm.toggle_display('employee', !frm.doc.__islocal);
    },
    employee: function (frm) {
      if (!frm.doc['employee']) {
        frm.set_value('employee_name', null);
      }
    },
    on_submit: function (frm) {
      frm.reload_doc();
    }
  };
  const lab_test_list = {
    has_indicator_for_draft: true,
    add_fields: ['docstatus', 'workflow_state', 'delivery_time'],
    get_indicator: function ({
      docstatus,
      workflow_state,
      delivery_time
    }) {
      if (docstatus === 1 && workflow_state === 'Completed' && moment().isAfter(delivery_time)) {
        return ['Delivered', 'black', `workflow_state,=,Completed|delivery_time,<,${frappe.datetime.now_datetime()}`];
      }

      return [workflow_state, get_color(workflow_state), `workflow_state,=,${workflow_state}`];
    }
  };

  // Copyright (c) 2018, Libermatic and contributors
  // For license information, please see license.txt
  const sales_invoice = {
    onload: function (frm) {
      if (frm.doc.docstatus === 1) {
        frm.add_custom_button('Lab Test', () => frappe.set_route('List', 'Lab Test', {
          invoice: frm.doc.name
        }), __('View'));
      }
    },
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
    physician,
    patient,
    lab_test_template,
    lab_test,
    lab_test_list,
    sales_invoice
  };

  var index$1 = {
    scripts
  };

  return index$1;

}());
