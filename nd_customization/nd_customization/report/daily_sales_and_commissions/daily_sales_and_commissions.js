// Copyright (c) 2016, Libermatic and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports['Daily Sales and Commissions'] = {
  filters: [
    {
      fieldname: 'from_date',
      label: 'From Date',
      fieldtype: 'Date',
      default: frappe.datetime.get_today(),
    },
    {
      fieldname: 'to_date',
      label: 'To Date',
      fieldtype: 'Date',
      default: frappe.datetime.get_today(),
    },
    {
      fieldname: 'patient',
      label: 'Patient ID',
      fieldtype: 'Link',
      options: 'Patient',
    },
    {
      fieldname: 'sales_partner',
      label: 'Sales Partner',
      fieldtype: 'Link',
      options: 'Sales Partner',
    },
  ],
};
