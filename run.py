# -*- coding: utf-8 -*-
# run.py
# License:   MIT License
# Author:    Roland Lucien Maxand
# Email:     r.maxand@outlook.com
# Copyright: (c) 2017 Roland Lucien Maxand

import os

from app import create_app


__project__ = 'Auxillary Flask-App'
__version__ = '0.1.2'
__author__ = 'Auxillary (gitaux)'
__repository__ = 'https://github.com/gitaux'
__copyright__ = 'copyright (c) 2017'

config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name='development')

if __name__ == '__main__':
    app.run()
