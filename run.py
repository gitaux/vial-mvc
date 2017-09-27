# -*- coding: utf-8 -*-
# run.py
#
# License:   MIT License
# Author:    Roland Lucien Maxand
# Email:     r.maxand@outlook.com
# Github:    https://github.com/gitaux
# Copyright: (c) 2017 Roland Lucien Maxand

import os

from app import create_app


__version__ = '0.1.0'

config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name='development')

if __name__ == '__main__':
    app.run()
