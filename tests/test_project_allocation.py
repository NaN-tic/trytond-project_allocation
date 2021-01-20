# This file is part project_allocation module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest


from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import suite as test_suite


class ProjectAllocationTestCase(ModuleTestCase):
    'Test Project Allocation module'
    module = 'project_allocation'


def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            ProjectAllocationTestCase))
    return suite
