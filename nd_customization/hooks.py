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
            'Sales Invoice-naming_series-options',
            'Sales Invoice-naming_series-default',
            'Sales Invoice-default_print_format',
            'Purchase Invoice-naming_series-options',
            'Purchase Invoice-naming_series-default',
            'Payment Entry-naming_series-options',
            'Payment Entry-naming_series-default',
            'Lab Test-naming_series-options',
            'Lab Test-naming_series-default',
            'Patient-quick_entry',
        ]]],
    },
    {
        'doctype': 'Custom Field',
        'filters': [['name', 'in', [
            'Patient-age_in_years',
            'Patient-location',
            'Sales Invoice-patient',
            'Sales Invoice-patient_name',
            'Sales Invoice-ref_physician',
            'Sales Invoice Item-reference_dt',
            'Sales Invoice Item-reference_dn',
        ]]]
    },
]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/nd_customization/css/nd_customization.css"
# app_include_js = "/assets/nd_customization/js/nd_customization.js"
app_include_js = '/assets/js/nd_customization.min.js'

# include js, css files in header of web template
# web_include_css = "/assets/nd_customization/css/nd_customization.css"
# web_include_js = "/assets/nd_customization/js/nd_customization.js"

# NOTE: disable all JS Includes in prod

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
    'Patient': 'public/js/cscripts/patient.js',
    'Sales Invoice': 'public/js/cscripts/sales_invoice.js',
}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
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
