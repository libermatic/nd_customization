# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__

app_name = "nd_customization"
app_version = __version__
app_title = "ND Customization"
app_publisher = "Libermatic"
app_description = "Customization for ND"
app_icon = "fa fa-flask"
app_color = "#E91E63"
app_email = "info@libermatic.com"
app_license = "MIT"

error_report_email = "support@libermatic.com"

fixtures = [
    {
        'doctype': 'Property Setter',
        'filters': [['name', 'in', [
            'Sales Invoice-project-hidden',
            'Sales Invoice-appointment-hidden',
            'Sales Invoice-naming_series-options',
            'Sales Invoice-naming_series-default',
            'Sales Invoice-default_print_format',
            'Sales Invoice Item-qty-in_list_view',
            'Sales Invoice Item-amount-in_list_view',
            'Sales Invoice Item-warehouse-in_list_view',
            'Sales Invoice Item-batch_no-in_list_view',
            'Sales Invoice Item-serial_no-in_list_view',
            'Purchase Invoice-naming_series-options',
            'Purchase Invoice-naming_series-default',
            'Payment Entry-naming_series-options',
            'Payment Entry-naming_series-default',
            'Sample Collection-naming_series-options',
            'Sample Collection-naming_series-default',
            'Lab Test-naming_series-options',
            'Lab Test-naming_series-default',
            'Lab Test-default_print_format',
            'Lab Test-invoice-in_standard_filter',
            'Lab Test-sample-in_standard_filter',
            'Lab Test Template-section_break_description-label',
            'Lab Test Template-section_break_description-collapsible',
            'Patient-dob-reqd',
            'Patient-mobile-reqd',
            'Healthcare Settings-require_test_result_approval-hidden',
            'Normal Test Template-test_uom-depends_on',
            'Normal Test Template-normal_range-depends_on',
        ]]],
    },
    {
        'doctype': 'Custom Field',
        'filters': [['name', 'in', [
            'Patient-age_in_years',
            'Patient-address_line1',
            'Sales Invoice-patient',
            'Sales Invoice-patient_name',
            'Sales Invoice-ref_physician',
            'Sales Invoice Item-reference_dt',
            'Sales Invoice Item-reference_dn',
            'Sales Invoice Item-lab_test_result_date',
            'Lab Test Template-naming_series',
            'Lab Test Template-test_comment',
            'Lab Test Template-test_custom_result',
            'Lab Test Template-sample_in_print',
            'Lab Test-sample_in_print',
            'Lab Test-delivery_time',
            'Healthcare Settings-templates_use_naming_series',
            'Normal Test Template-is_subsection',
        ]]],
    },
    {
        'doctype': 'Workflow',
        'filters': [['name', 'in', [
            'Lab Test Workflow',
        ]]],
    },
    {
        'doctype': 'Workflow State',
        'filters': [['name', 'in', [
            'Pending',
            'Discarded',
            'Completed',
            'Approved',
            'Rejected',
            'Cancelled',
        ]]],
    },
    {
        'doctype': 'Workflow Action',
        'filters': [['name', 'in', [
            'Reject',
            'Submit',
            'Approve',
            'Cancel',
        ]]],
    },
]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/nd_customization/css/nd_customization.css"
# app_include_js = "/assets/nd_customization/js/nd_customization.js"
app_include_js = '/assets/nd_customization/js/nd_customization.iife.js'

# include js, css files in header of web template
# web_include_css = "/assets/nd_customization/css/nd_customization.css"
# web_include_js = "/assets/nd_customization/js/nd_customization.js"

# NOTE: disable all JS Includes in prod

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
    'Physician': 'public/js/cscripts/physician.js',
    'Patient': 'public/js/cscripts/patient.js',
    'Lab Test Template': 'public/js/cscripts/lab_test_template.js',
    'Lab Test': 'public/js/cscripts/lab_test.js',
    'Sales Invoice': 'public/js/cscripts/sales_invoice.js',
}
doctype_list_js = {
    'Lab Test': 'public/js/cscripts/lab_test_list.js',
}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#    "Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "nd_customization.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "nd_customization.install.before_install"
# after_install = "nd_customization.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = \
#   "nd_customization.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#     "Event":
#       "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#     "Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    'Lab Test Template': {
        'autoname': 'nd_customization.doc_events.lab_test_template.autoname',
    },
    'Lab Test': {
        'validate': 'nd_customization.doc_events.lab_test.validate',
        'after_insert': 'nd_customization.doc_events.lab_test.after_insert',
        'before_cancel': 'nd_customization.doc_events.lab_test.before_cancel',
        'on_update_after_submit':
            'nd_customization.doc_events.lab_test.on_update_after_submit',
    },
    'Sales Invoice': {
        'validate': 'nd_customization.doc_events.sales_invoice.validate',
        'on_submit': 'nd_customization.doc_events.sales_invoice.on_submit',
        'on_cancel': 'nd_customization.doc_events.sales_invoice.on_cancel',
    },
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
#     "all": [
#         "nd_customization.tasks.all"
#     ],
#     "daily": [
#         "nd_customization.tasks.daily"
#     ],
#     "hourly": [
#         "nd_customization.tasks.hourly"
#     ],
#     "weekly": [
#         "nd_customization.tasks.weekly"
#     ]
#     "monthly": [
#         "nd_customization.tasks.monthly"
#     ]
# }

# Testing
# -------

# before_tests = "nd_customization.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
#     "frappe.desk.doctype.event.event.get_events":
#            "nd_customization.event.get_events"
# }
