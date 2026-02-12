from odoo import models, api
from odoo.tools.safe_eval import safe_eval, datetime, dateutil, time
from odoo.addons.base.models import ir_model
from odoo.exceptions import ValidationError

SAFE_EVAL_BASE = {
    'datetime': datetime,
    'dateutil': dateutil,
    'time': time,
}

def sum_c(self, name, range2):
    fields = range2.split(':')

    for record in self:
        total = 0
        for field in fields:
            total += record[field] or 0
        record[name] = total

def product_c(self, name, range2):
    fields = range2.split(':')

    for record in self:
        total = 1
        for field in fields:
            total *= record[field] or 0
        record[name] = total

def make_compute_patched(text, deps):

    def func(self):
        ctx = SAFE_EVAL_BASE.copy()
        ctx.update({
            'self': self,
            'SUM': lambda name, range2: sum_c(self, name, range2),
            'PRODUCT': lambda name, range2: product_c(self, name, range2),
        })
        return safe_eval(text, ctx, mode="exec")

    deps = [d.strip() for d in deps.split(",")] if deps else []
    return api.depends(*deps)(func)

# 🔥 monkey patch
ir_model.make_compute = make_compute_patched

class IrActionsServer(models.Model):
    _inherit = 'ir.actions.server'

    def _get_eval_context(self, action=None):
        eval_context = super()._get_eval_context(action=action)

        eval_context.update({
            'CREATE_OR_WRITE': lambda _name, fields, data: self.create_or_write(_name, fields, data),

        })
        return eval_context

    def create_or_write(self, model_name, fields, values):
        model = self.env[model_name]

        domain = []
        for field in fields.split(','):
            field = field.strip()
            domain.append((field, '=', values.get(field)))

        record = model.search(domain, limit=1)
        if record:
            record.write(values)
            return record
        else:
            return model.create(values)
