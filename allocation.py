# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond.model import ModelView, ModelSQL, fields
from trytond.pool import PoolMeta
from trytond.pyson import Eval


__all__ = ['Allocation']


class Allocation(ModelSQL, ModelView):
    'Allocation'
    __name__ = 'project.allocation'
    employee = fields.Many2One('company.employee', 'Employee', required=True,
            domain=[
                ('company', '=', Eval('company')),
            ], depends=['company'], select=True, ondelete='CASCADE')
    work = fields.Many2One('project.work', 'Work', required=True,
            select=True, ondelete='CASCADE')
    company = fields.Function(fields.Many2One('company.company', 'Company'),
        'on_change_with_company', searcher='search_company')

    def get_rec_name(self, name):
        return self.employee.rec_name

    @classmethod
    def search_rec_name(cls, name, clause):
        return [('employee.rec_name',) + tuple(clause[1:])]

    @fields.depends('work', '_parent_work.company')
    def on_change_with_company(self, name=None):
        if self.work and self.work.company:
            return self.work.company.id

    @classmethod
    def search_company(cls, name, clause):
        return [('work.company',) + tuple(clause[1:])]


class Work(metaclass=PoolMeta):
    __name__ = 'project.work'
    allocations = fields.One2Many('project.allocation', 'work', 'Allocations')
    employees = fields.Function(fields.Char('Employees'), 'get_employees',
        searcher='search_employees')

    @classmethod
    def __setup__(cls):
        super(Work, cls).__setup__()
        readonly = Eval('allocations', [0])
        if 'readonly' in cls.company.states:
            cls.company.states['readonly'] |= readonly
        else:
            cls.company.states['readonly'] = readonly

    def get_employees(self, name):
        return ', '.join(sorted([x.employee.rec_name for x in
                    self.allocations]))

    @classmethod
    def search_employees(cls, name, clause):
        return [('allocations.employee',) + tuple(clause[1:])]
