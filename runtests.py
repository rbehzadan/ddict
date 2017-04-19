#!/usr/bin/env python

__author__ = 'Reza Behzadan'
__email__ = 'rbehzadan@gmail.com'
__copyright__ = 'Copyright © 2017 Reza Behzadan'
__date__ = '2017-04-19'

__license__ = 'MIT'
__version__ = '0.0.1'
__status__ = 'development'


import socket
import sys

import coverage
import pytest

cov = coverage.coverage(branch=True, include='ddict/*')
cov.set_option('report:show_missing', True)
cov.start()

pytest.main(["tests"])

cov.stop()
cov.report()


