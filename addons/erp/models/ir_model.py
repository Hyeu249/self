from odoo import models, fields, api
from odoo.exceptions import ValidationError
import uuid
from odoo.fields import Command, Domain
import xml.etree.ElementTree as ET
import os

class IrModel(models.Model):
    _inherit = "ir.model"
    def _default_field_id(self):
        if self.env.context.get('install_mode'):
            return []                   # no default field when importing
        return [Command.create({'name': 'x_name', 'field_description': 'Name', 'ttype': 'char', 'copied': True})]

    field_id = fields.One2many(
        'ir.model.fields',
        'model_id', string='Fields',
        required=True, copy=True,
        domain=lambda self: self._get_field_id_domain(),
        default=_default_field_id
    )
    is_filter_manual = fields.Boolean(
        string="Is Filter Manual",
    )
    from_app_id = fields.Many2one(
        'erp.custom.app',
        string='From App',
    )

    def _get_field_id_domain(self):
        for record in self:
            if record.is_filter_manual:
                return [('state', '=', 'manual')]
            else:
                return []

    server_action_count = fields.Integer(
        compute="_compute_server_action_count"
    )

    view_count = fields.Integer(
        string="Views",
        compute="_compute_view_count"
    )
    base_automation_count = fields.Integer(
        string="Automations",
        compute="_compute_base_automation_count"
    )
    scheduled_action_count = fields.Integer(
        string="Scheduled Actions",
        compute="_compute_scheduled_action_count"
    )
    menu_count = fields.Integer(
        string="Menus",
        compute="_compute_menu_count"
    )

    def _compute_menu_count(self):
        ActWindow = self.env['ir.actions.act_window']
        Menu = self.env['ir.ui.menu']

        for rec in self:
            actions = ActWindow.search([
                ('res_model', '=', rec.model)
            ])
            if actions:
                action_names = [
                    f"ir.actions.act_window,{a.id}" for a in actions
                ]
                rec.menu_count = Menu.search_count([
                    ('action', 'in', action_names)
                ])
            else:
                rec.menu_count = 0

    def _compute_scheduled_action_count(self):
        Cron = self.env['ir.cron']
        for rec in self:
            rec.scheduled_action_count = Cron.search_count([
                ('model_id', '=', rec.id)
            ])

    def _compute_base_automation_count(self):
        Automation = self.env['base.automation']
        for rec in self:
            rec.base_automation_count = Automation.search_count([
                ('model_id', '=', rec.id)
            ])

    def _compute_view_count(self):
        View = self.env['ir.ui.view']
        for rec in self:
            rec.view_count = View.search_count([
                ('model', '=', rec.model)
            ])

    def _compute_server_action_count(self):
        for rec in self:
            rec.server_action_count = self.env['ir.actions.server'].search_count([
                ('model_id', '=', rec.id)
            ])


    def action_view_server_actions(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Server Actions',
            'res_model': 'ir.actions.server',
            'view_mode': 'list,form',
            'domain': [('model_id', '=', self.id)],
            'context': {'default_model_id': self.id},
        }

    def action_view_views(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Views',
            'res_model': 'ir.ui.view',
            'view_mode': 'list,form',
            'domain': [('model', '=', self.model)],
            'context': {'default_model': self.model},
        }

    def action_view_base_automation(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Views',
            'res_model': 'base.automation',
            'view_mode': 'list,form',
            'domain': [('model_id', '=', self.id)],
            'context': {'default_model_id': self.id},
        }
    def action_view_scheduled_actions(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Scheduled Actions',
            'res_model': 'ir.cron',
            'view_mode': 'list,form',
            'domain': [('model_id', '=', self.id)],
            'context': {'default_model_id': self.id},
        }
    def action_view_menus(self):
        self.ensure_one()
        actions = self.env["ir.actions.act_window"].search([('res_model', '=', self.model)])
        action_names = [f"ir.actions.act_window,{a.id}" for a in actions]

        return {
            'type': 'ir.actions.act_window',
            'name': 'Menus',
            'res_model': 'ir.ui.menu',
            'view_mode': 'list,form',
            'domain': [('action', 'in', action_names)],
            'context': {'default_action': action_names[0] if action_names else False},
        }

    def create_fields_py_str(self):
        strs = ""
        fields = sorted(
            self.field_id,
            key=lambda f: bool(f.related or f.depends)
        )
        for field in fields:
            vals = field.read()[0]
            new_vals = {}
            for f in ['name', 'field_description', 'ttype', 'help', 'sequence', 'relation', 'relation_field', 'relation_table', 'column1', 'column2', 'on_delete', 'domain', 'related', 'depends', 'compute', 'required', 'readonly', 'invisible', 'store', 'index', 'copied', 'tracking', 'approval_field']:
                new_vals[f] = vals.get(f)
            strs += f'''
        vals = {new_vals}
        vals['model_id'] = model_id.id
        field_id = env['ir.model.fields'].create(vals)
'''
            for selection in field.selection_ids:
                vals = selection.read()[0]
                new_vals = {}
                for f in ['sequence', 'value', 'name']:
                    new_vals[f] = vals.get(f)
                strs += f'''
        vals = {new_vals}
        vals['field_id'] = field_id.id
        env['{selection._name}'].create(vals)
'''

            for group in field.groups:
                strs += f'''
        group_id = env['{group._name}'].search([('name', '=', '{group.name}')], limit=1)
        if not group_id:
            raise ValidationError('Group {group.name} not found, please create it first.')
'''
            strs += f'''
        field_id.groups = [(4, {field.groups.ids})]
'''
        return strs

    def create_model_py_str(self):
        vals = self.read()[0]
        new_vals = {}
        for f in ['name', 'model', 'state', 'transient', 'is_filter_manual', 'is_mail_thread', 'is_mail_activity']:
            new_vals[f] = vals.get(f)
        return f'''
    def {self.model}():
        """{self.name}"""
        vals = {new_vals}
        vals['from_app_id'] = custom_module_id.id if custom_module_id else False
        model_id = env['ir.model'].create(vals)
        x_name = env['ir.model.fields'].search([('model_id', '=', model_id.id), ('name', '=', 'x_name')], limit=1)
        if x_name:
            x_name.unlink()
'''

    def create_model_access_right_py_str(self):
        strs = ""
        for access in self.access_ids:
            vals = access.read()[0]
            new_vals = {}
            for f in ['name', 'perm_read', 'perm_write', 'perm_create', 'perm_unlink']:
                new_vals[f] = vals.get(f)
            strs += f'''
        vals = {new_vals}
        group_id = env['{access.group_id._name}'].search([('name', '=', '{access.group_id.name}')], limit=1)
        if not group_id:
            raise ValidationError('Group {access.group_id.name} not found, please create it first.')

        vals['group_id'] = {access.group_id.id}
        vals['model_id'] = model_id.id
        env['{access._name}'].create(vals)
'''
        return strs

    def transfer_to_python_str(self):
        return f'''
        {self.create_model_py_str()}
        {self.create_model_access_right_py_str()}
        {self.create_fields_py_str()}
    {self.model}()
'''
