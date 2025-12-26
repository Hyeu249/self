from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Build(models.TransientModel):
    _name = 'erp.build'
    _description = 'Build'

    name = fields.Char(string="Name")
    description = fields.Text(string="Description")

    def action_confirm(self):
        raise ValidationError("Build confirmed: %s" % self.name)
