#!/usr/bin/env python
import sys
sys.path[0] = sys.path[0] + "/.."

import unittest

import define

testmodules = [
    "tests.test_rsa",
    "tests.test_alipay",
    "tests.test_handlers.test_wap",
    "tests.test_models.test_trade",
    "tests.test_models.test_product",
    "tests.test_models.test_applog"
]


def init_suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests([loader.loadTestsFromName(m) for m in testmodules])
    return suite

if __name__ == '__main__':
    suite = init_suite()
    unittest.TextTestRunner(verbosity=2).run(suite)