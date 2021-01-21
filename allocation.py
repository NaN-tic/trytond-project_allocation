# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond.model import ModelView, ModelSQL, fields, tree
from trytond.pool import PoolMeta
from trytond.pyson import Eval

__all__ = ['Allocation']


class Allocation(ModelSQL, ModelView):
    'Allocation'
    __name__ = 'project.allocation'
    employee = fields.Many2One('company.employee', 'Employee', required=True,
            select=True, ondelete='CASCADE')
    work = fields.Many2One('project.work', 'Work', required=True,
            select=True, ondelete='CASCADE')

    def get_rec_name(self, name):
        return self.employee.rec_name

    @classmethod
    def search_rec_name(cls, name, clause):
        return [('employee.rec_name',) + tuple(clause[1:])]


class Work(metaclass=PoolMeta):
    __name__ = 'project.work'
    allocations = fields.One2Many('project.allocation', 'work', 'Allocations',
        states={
            'invisible': Eval('type') != 'task',
            }, depends=['type'])
    employees = fields.Function(fields.Char('Employees'), 'get_employees',
        searcher='search_employees')

    def get_employees(self, name):
        return ', '.join(sorted([x.employee.rec_name for x in
                    self.allocations]))

    @classmethod
    def search_employees(cls, name, clause):
        return [('allocations.employee',) + tuple(clause[1:])]
