# -*- coding:utf-8 -*-
from setuptools import setup, find_packages
import sys

sys.path.append('./lib')
sys.path.append('./test')
sys.path.append('/opt/tornado')

setup(
    name         = "tornado www server",
    author       = "Nobuaki Mochizuki",
    author_email = "motizuki_nobuaki_gn@microad.co.jp",
    license      = "GPL",
    description  = "README",
    version      = "0.1-alpha",
    packages     = find_packages(),
    test_suite   = 'tornado_test.suite'
)


