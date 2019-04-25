// Copyright (c) 2018, Libermatic and contributors
// For license information, please see license.txt

frappe.ui.form.on('Lab Test', nd_customization.scripts.lab_test);

// Move the validation done by this block to before_submit hook
cur_frm.cscript.custom_before_submit = () => {};
