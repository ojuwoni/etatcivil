# -*- coding: utf-8 -*-

"""
Django settings for the alessandria app.
"""

from django.conf import settings
from django.db.utils import OperationalError

context_processors = settings.TEMPLATES[0]['OPTIONS']['context_processors']
# Used for i18n of jquery date picker plugin (http://keith-wood.name/datepick.html)
context_processors.append("gestciv.context_processors.js_datepicker_lang")
context_processors.append("gestciv.context_processors.app_version")
context_processors.append("gestciv.context_processors.library_infos")

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'gestciv.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers':['file'],
            'propagate': True,
            'level':'INFO',
        },
        'gestciv': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    }
}
