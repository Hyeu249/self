from odoo import models, fields, api
from odoo.exceptions import ValidationError
import uuid
from odoo.fields import Command, Domain

title = {
    '1': 'Pick Options',
    '2': 'Please create your model name',
    '3': 'Please set menu',
    '4': 'Please pick your model',
}
previous_stage = {
    '2': '1',
    '3': '2',
    '4': '1',
}

class IrUiView(models.Model):
    _inherit = "ir.ui.view"

    def update_view(self):
        if self.type == 'list':
            return self.update_list_view()
        elif self.type == 'form':
            return self.update_form_view()
        elif self.type == 'search':
            return self.update_search_view()

    def get_custom_fields(self):
        return self.model_id.field_id.filtered(lambda f: f.state == 'manual').sorted(key=lambda self: self.sequence)

    def update_list_view(self):
        one2many = lambda s: s.ttype == "one2many"

        field_ids = self.get_custom_fields()
        normal_field_ids = field_ids.filtered(lambda s: not one2many(s))
        one2many_fields = field_ids.filtered(one2many)
        field_tags = [f"<field name='{field.name}' optional='show'/>\n" for field in normal_field_ids]
        one2many_tags = [
            f"<field name='{field.name}' widget='many2many_tags' optional='show'/>\n"
            for field in one2many_fields
        ]

        self.arch_base = f"""
            <list>
                {''.join(field_tags)}
                {''.join(one2many_tags)}
            </list>
        """

    def update_form_view(self):
        return

    def update_search_view(self):
        return

class IrUiMenu(models.Model):
    _inherit = "ir.ui.menu"

    is_custom = fields.Boolean(string="Is Custom")

class IrModelFields(models.Model):
    _inherit = "ir.model.fields"

    sequence = fields.Integer("Sequence")
    selected_model_id = fields.Many2one(
        'ir.model', 
        string='Model',
        domain=[('state', '=', "manual")],
    )
    selected_field_id = fields.Many2one(
        'ir.model.fields',
        string='Relation Field',
        domain="[('state', '=', 'manual'), ('model_id', '=', selected_model_id)]"
    )
    @api.onchange('selected_model_id')
    def _onchange_selected_model_id(self):
        for record in self:
            if record.selected_model_id:
                record.relation = record.selected_model_id.model
            else:
                record.relation = ""
    @api.onchange('selected_field_id')
    def _onchange_selected_field_id(self):
        for record in self:
            if record.selected_field_id:
                record.relation_field = record.selected_field_id.name
            else:
                record.relation_field = ""

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
    def _get_field_id_domain(self):
        if self.is_filter_manual:
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
        if actions:
            action_name = f"ir.actions.act_window,{actions[0].id}"
            return {
                'type': 'ir.actions.act_window',
                'name': 'Menus',
                'res_model': 'ir.ui.menu',
                'view_mode': 'list,form',
                'domain': [('action', '=', action_name)],
                'context': {'default_action': action_name},
            }

class Build(models.TransientModel):
    _name = 'erp.build'
    _description = 'Build'

    action_type = fields.Selection(
            selection=[
                ('create', 'Create'),
                ('edit', 'Edit'),
                ('delete', 'Delete'),
            ],
            string='Action',
            default='edit',
            required=True,
        )
    mode = fields.Selection(
            selection=[
                ('model', 'Model'),
                ('menu', 'Menu'),
            ],
            string='Mode',
            default='model',
            required=True,
            readonly=True,
        )
    stage = fields.Selection(
            selection=[
                ('1', '1'),
                ('2', '2'),
                ('3', '3'),
                ('4', '4'),
            ],
            string='Action',
            default='1',
            required=True,
        )
    model_description = fields.Char(string='Name')
    model_name = fields.Char(
        string='Name', 
        default=lambda self: f"x_{uuid.uuid4().hex}",
    )
    model_id = fields.Many2one(
        "ir.model",
        string="Model",
        domain=[('state', '=', "manual")],
    )
    menu_id = fields.Many2one(
        "ir.ui.menu",
        string="Menu",
        domain=[('parent_id', '!=', False), ('is_custom', '=', True), ('action', '=', False)],
    )
    parent_menu_id = fields.Many2one(
        "ir.ui.menu",
        string="Parent Menu",
        domain=[('parent_id', '=', False), ('is_custom', '=', True)],
    )

    def go_to_stage(self):
        return {
            'type': 'ir.actions.act_window',
            'name': title.get(self.stage),
            'res_model': 'erp.build',
            'view_mode': 'form',
            'target': 'new',

            'res_id': self.id,
            'context': {
                **self.env.context,
            },
        }
    def confirm_stage_1(self):
        if self.action_type == 'delete':
            self.stage = '4'
        elif self.action_type == 'edit':
            self.stage = '4'
        else:
            self.stage = '2'

        return self.go_to_stage()

    def confirm_stage_2(self):
        self.stage = '3'
        return self.go_to_stage()

    def confirm_stage_3(self):
        self.create_model(self.model_description, self.model_name)
        self.create_tree_view_id(self.model_name)
        self.create_form_view_id(self.model_name)
        self.create_search_view_id(self.model_name)
        self.create_menu(self.model_description, self.model_name, self.menu_id.id)
        self.menu_id.parent_id = self.parent_menu_id.id
    
    def delete_model(self):
        actions = self.env["ir.actions.act_window"].search([('res_model', '=', self.model_id.model)])
        if actions:
            menus = self.env['ir.ui.menu'].search([('action', '=', f"ir.actions.act_window,{actions[0].id}")])
            menus.unlink()
            actions.unlink()
        self.model_id.view_ids.unlink()
        self.model_id.unlink()

    def confirm_stage_4(self):
        if self.action_type == 'delete':
            self.delete_model()
        elif self.action_type == 'edit':
            return self.action_open_ir_model()

    def action_open_ir_model(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "IR Model",
            "res_model": "ir.model",
            "view_mode": "form",
            "view_id": self.env.ref("erp.view_erp_ir_model_form").id,
            "res_id": self.model_id.id,
            "target": "current",
        }

    def previous(self):
        self.stage = previous_stage.get(self.stage, '1')
        return self.go_to_stage()

    def create_model(self, name, model):
        model_id = self.env['ir.model'].create(
            {
                "name": name,
                "model": model,
                "state": "manual",
                "is_mail_thread": True,
                "is_mail_activity": True,
                "is_filter_manual": True
            }
        )

        self.env["ir.model.access"].create(
            {
                "name": f"access_{model}_user",
                "model_id": model_id.id,
                "group_id": self.env.ref("base.group_user").id,
                "perm_read": True,
                "perm_write": True,
                "perm_create": True,
                "perm_unlink": True,
            }
        )

        return model

    def create_menu(self, name, model, parent_menu_id):
        action_id = self.create_model_act_window(name, model)

        return self.env["ir.ui.menu"].create(
            {
                "name": name,
                "parent_id": parent_menu_id,
                "action": f"ir.actions.act_window,{action_id.id}",
                "is_custom": True,
            }
        )

    def create_model_act_window(self, name, model):
        action = self.env["ir.actions.act_window"].create(
            {
                "name": name,
                "res_model": model,
                "type": "ir.actions.act_window",
                "view_mode": "list,form",
                "target": "current",
            }
        )
        return action

    def create_tree_view_id(self, model_name):
        return self.env['ir.ui.view'].create(
            {
                "name": model_name + ".list",
                "model": model_name,
                "arch_base": """
                    <list>
                        <field name="x_name"/>
                    </list>
                """,
            }
        )

    def create_form_view_id(self, model_name):
        return self.env['ir.ui.view'].create(
            {
                "name": model_name + ".form",
                "model": model_name,
                "arch_base": """
                    <form>
                        <sheet>
                        <group>
                            <field name="x_name"/>
                        </group>
                        </sheet>
                        <chatter/>
                    </form>
                """,
            },
        )

    def create_search_view_id(self, model_name):
        return self.env['ir.ui.view'].create(
            {
                "name": model_name + ".search",
                "model": model_name,
                "arch_base": """<search><field name="x_name"/></search>""",
            },
        )
