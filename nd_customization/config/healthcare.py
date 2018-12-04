# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _


def get_data():
    return [
        {
            'label': _('Masters'),
            'items': [
                {
                    'type': 'doctype',
                    'name': 'Lab Test Center',
                    'label': 'Test Center',
                },
            ]
        },
        {
            'label': _('Setup'),
            'items': [
                {
                    'type': 'doctype',
                    'name': 'ND Settings',
                    'label': 'ND Settings',
                },
            ]
        },
    ]
