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
            'GET_FIFO': lambda lines, basic_rate: self.calc_fifo(lines, basic_rate),
            'SEARCH_READ': lambda model_name=False, **args: self.search_read_data(model_name, **args),
            'WRITE': lambda id, data, model_name=False: self.write_record(id, data, model_name=model_name),

        })
        return eval_context
    
    def search_read_data(self, model_name=False, **args):
        if not model_name:
            model_name = self.model_id.model
        model = self.env[model_name]
        return model.search_read(**args)

    def write_record(self, id, data, model_name=False):
        if not model_name:
            model_name = self.model_id.model
        record = self.env[model_name].browse(id)
        record.write(data)

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

    def calc_fifo(self, lines, basic_rate=120000):
        fifo = []
        result = []

        for line in lines:
            if line['x_sl'] > 0:
                fifo.append({
                    'qty': line['x_sl'],
                    'price': line['x_gia_von'],
                })

            elif line['x_sl'] < 0:
                need = -line['x_sl']
                cost = 0.0

                # lấy FIFO trước
                for lot in fifo:
                    if need <= 0:
                        break

                    take = min(need, lot['qty'])
                    cost += take * lot['price']
                    lot['qty'] -= take
                    need -= take

                # nếu còn dư → tính theo basic_rate
                if need > 0:
                    cost += need * basic_rate

                fifo_price = cost / -line['x_sl']

                # chỉ trả nếu GIÁ SAI
                if round(line['x_gia_von'], 2) != round(fifo_price, 2):
                    new_line = dict(line)
                    new_line['x_gia_von'] = fifo_price
                    result.append(new_line)

        return result
