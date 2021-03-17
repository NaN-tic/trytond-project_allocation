# This file is part project_allocation module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import allocation


def register():
    Pool.register(
        allocation.Allocation,
        allocation.Work,
        module='project_allocation', type_='model')
