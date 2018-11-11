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
        'doctype': 'Custom Field',
        'filters': [['name', 'in', [
            'Patient-age_in_years',
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

# include js, css files in header of web template
# web_include_css = "/assets/nd_customization/css/nd_customization.css"
# web_include_js = "/assets/nd_customization/js/nd_customization.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
    'Patient': 'public/js/patient.js',
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

# doc_events = {
#     "*": {
#         "on_update": "method",
#         "on_cancel": "method",
#         "on_trash": "method"
#    }
# }

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
