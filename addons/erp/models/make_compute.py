from dataclasses import fields
from odoo import models, api
from odoo.tools.safe_eval import safe_eval, datetime, dateutil, time
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

def minus_c(self, name, range2):
    fields = range2.split(':')

    for record in self:
        total = record[fields[0]] or 0
        for field in fields[1:]:
            total -= record[field] or 0
        record[name] = total

def product_c(self, name, range2):
    fields = range2.split(':')

    for record in self:
        total = 1
        for field in fields:
            total *= record[field] or 0
        record[name] = total

def sum_col(self, name, sum_field, relation):

    for record in self:
        total = record[relation].mapped(sum_field)
        record[name] = sum(total)

def fnc(self, name, lb):

    for record in self:
        record[name] = lb(record)

def make_compute_patched(field_name, text, deps):

    def func(self):
        ctx = SAFE_EVAL_BASE.copy()
        ctx.update({
            'self': self,
            'SUM': lambda range2: sum_c(self, field_name, range2),
            'MINUS': lambda range2: minus_c(self, field_name, range2),
            'PRODUCT': lambda range2: product_c(self, field_name, range2),
            'SUM_COL': lambda sum_field, relation: sum_col(self, field_name, sum_field, relation),
            'SET': lambda lb: fnc(self, field_name, lb),
        })
        return safe_eval(text, ctx, mode="exec")

    deps = [d.strip() for d in deps.split(",")] if deps else []
    return api.depends(*deps)(func)

class IrModelFields(models.Model):
    _inherit = 'ir.model.fields'

    def _instanciate_attrs(self, field_data):
        attrs = super(IrModelFields, self)._instanciate_attrs(field_data=field_data)

        if field_data['compute']:
            attrs['compute'] = make_compute_patched(field_data["name"], field_data['compute'], field_data['depends'])

        return attrs

class IrActionsServer(models.Model):
    _inherit = 'ir.actions.server'

    def _get_eval_context(self, action=None):
        eval_context = super()._get_eval_context(action=action)
        record = eval_context.get('record')

        eval_context.update({
            'SEARCH_READ': lambda model_name=False, **args: self.search_read_data(model_name, **args),
            'WRITE': lambda id, data, model_name=False: self.write_record(id, data, model_name=model_name),
            'CREATE_OR_WRITE': lambda model_name, fields, data: self.create_or_write(model_name, fields, data),
            "EXPAND_ARRAY": lambda model_name, map_str, domain=False: self.expand_array(model_name, map_str, domain, record),
            "ACT_WINDOW": lambda id: self.env['ir.actions.act_window'].browse(id),
            "UNIQUE_MODEL": lambda name: self.get_model(name),
            "DELETE": lambda model_name, domain=False: self.delete_records(model_name, domain),
            "DISPLAY_SEQUENCE" : lambda: self.display_sequence(record),
            "REF_ID" : f"{record._name},{record.id}" if record else False,
            "REF" : lambda model, id: f"{model},{id}",
        })
        return eval_context

    def display_sequence(self, record):
        sequence = self.env['ir.sequence'].search([('code', '=', record._description)], limit=1)
        record.write({"x_name": sequence.get_next_char(sequence.number_next_actual)})

    def get_model(self, model_name):
        t = self.env["ir.model"].search([('name', '=', model_name)], limit=1)
        return self.env[t.model] if t else None
    
    def delete_records(self, model_name, domain):
        model = self.get_model(model_name)
        records = model.search(domain)
        records.unlink()

    def expand_array(self, model_name, map_str, domain2, record=None):
        data = {
            k.strip(): v.strip()
            for k, v in (p.split(":", 1) for p in map_str.split(","))
        }
        value = data.get("value")
        duplicate = data.get("duplicate")
        before = data.get("before")

        domain = []
        order = "id"
        fields = [value]

        if duplicate:
            fields.append(duplicate)
        if before:
            domain.append((before, '<', record[before]))
            order = f"{before}, id"
        if domain2:
            for v in domain2:
                domain.append(v)

        lines = self.get_model(model_name).search_read(
            domain=domain,
            fields=fields,
            order=order
        )
        arr = []

        for line in lines:
            a = line[value]
            c = [a]
            if duplicate:
                b = int(line[duplicate])
                c = [a * b / abs(b)] * abs(b)

            arr.extend(c)

        return arr

    def search_read_data(self, model_name=False, **args):
        if not model_name:
            model_name = self.model_id.name

        model = self.get_model(model_name)
        return model.search_read(**args)

    def write_record(self, id, data, model_name=False):
        if not model_name:
            model_name = self.model_id.name

        record = self.get_model(model_name).browse(id)
        record.write(data)

    def create_or_write(self, model_name, fields, values):
        model = self.get_model(model_name)

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

class IrActionsAct_window(models.Model):
    _inherit = 'ir.actions.act_window'

    def open(self):
        return self.read()[0]
    
class IrSequence(models.Model):
    _inherit = 'ir.sequence'

    @api.onchange("name")
    def _onchange_code(self):
        for record in self:
            record.code = record.name
