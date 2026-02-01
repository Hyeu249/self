from odoo import models, fields, api
from odoo.exceptions import ValidationError
import uuid
from odoo.fields import Command, Domain
import xml.etree.ElementTree as ET
import os

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

class IrUiMenu(models.Model):
    _inherit = "ir.ui.menu"

    is_custom = fields.Boolean(string="Is Custom")

class IrModelFields(models.Model):
    _inherit = "ir.model.fields.selection"

    selected_model_id = fields.Many2one(
        'ir.model', 
        string='Model',
        domain=[('state', '=', 'manual')]
    )

    @api.onchange('selected_model_id')
    def _onchange_selected_model_id(self):
        for record in self:
            if record.selected_model_id:
                record.value = record.selected_model_id.model
                record.name = record.selected_model_id.name
            else:
                record.value = ""
                record.name = ""

    @api.onchange('value')
    def _onchange_value(self):
        for record in self:
            if record.selected_model_id:
                return

            if record.value:
                record.name = record.value
            else:
                record.name = ""

class IrModelFields(models.Model):
    _inherit = "ir.model.fields"

    invisible = fields.Boolean("Invisible", default=False)
    approval_field = fields.Boolean("Approval Field", default=False)
    sequence = fields.Integer("Sequence")
    selected_model_id = fields.Many2one(
        'ir.model', 
        string='Model',
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

    def has_field(self, root, field_name):
        for field in root.iter("field"):
            if field.attrib.get("name") == field_name:
                return True
        return False

    def update_view(self):
        views = self.env['ir.ui.view'].search([('model', '=', self.model_id.model)])
        t_field = self.env['ir.model.fields'].search([
            ('model', '=', self.model_id.model),
            ('state', '=', 'manual'),
            ('sequence', '<=', self.sequence - 1)
            ], 
        order='sequence desc',
        limit=1)
        for view in views:
            parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True))
            root = ET.fromstring(view.arch_base, parser=parser)
            if self.has_field(root, self.name):
                continue
            for parent in root.iter():
                children = list(parent)

                for i, child in enumerate(children):
                    if child.tag == "field" and child.attrib.get("name") == t_field.name:

                        new_field = ET.Element("field", {
                            "name": self.name
                        })
                        if view.type == "list":
                            if self.ttype in ["many2many", "one2many"]:
                                new_field.set("widget", "many2many_tags")
                            new_field.set("optional", "show")

                        parent.insert(i + 1, new_field)

                        break
            ET.indent(root, space="    ")
            new_xml = ET.tostring(root, encoding="unicode")
            view.arch_base = new_xml

    def comment_field_view(self, new_name, old_name):
        views = self.env['ir.ui.view'].search([('model', '=', self.model_id.model)])
        for view in views:
            parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True))
            root = ET.fromstring(view.arch_base, parser=parser)

            if self.has_field(root, new_name):
                continue
            for parent in root.iter():
                children = list(parent)

                for i, child in enumerate(children):
                    if child.tag == "field" and child.attrib.get("name") == old_name:

                        child.set("name", new_name)
                        full_tag = ET.tostring(child, encoding="unicode").strip()
                        comment = ET.Comment(f"WHATSUP,{full_tag}")

                        parent.insert(i, comment)
                        parent.remove(child)
            ET.indent(root, space="    ")
            new_xml = ET.tostring(root, encoding="unicode")

            view.arch_base = new_xml

    def uncomment_field_view(self):
        views = self.env['ir.ui.view'].search([('model', '=', self.model_id.model)])
        for view in views:
            parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True))
            root = ET.fromstring(view.arch_base, parser=parser)
            for parent in root.iter():
                children = list(parent)
                for i, child in enumerate(children):
                    if child.tag is ET.Comment:
                        text = (child.text or "").strip()
                        if not text.startswith("WHATSUP,"):
                            continue
                        text = text.replace("WHATSUP,", "", 1).strip()
                        parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True))
                        field = ET.fromstring(text, parser=parser)
                        if field.tag == "field" and field.attrib.get("name") == self.name:
                            parent.insert(i, field)
                            parent.remove(child)

            ET.indent(root, space="    ")
            new_xml = ET.tostring(root, encoding="unicode")
            view.arch_base = new_xml

    def remove_field_view(self):
        views = self.env['ir.ui.view'].search([('model', '=', self.model_id.model)])
        for view in views:
            parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True))
            root = ET.fromstring(view.arch_base, parser=parser)
            for parent in root.iter():
                children = list(parent)
                for i, child in enumerate(children):
                    if child.tag == "field" and child.attrib.get("name") == self.name:
                        parent.remove(child)

            ET.indent(root, space="    ")
            new_xml = ET.tostring(root, encoding="unicode")
            view.arch_base = new_xml

    def write(self, vals):
        is_comment = False
        if "name" in vals:
            new_name = vals['name']
            for record in self:
                old_name = record.name
                if 'name' in vals and old_name != new_name:
                    record.comment_field_view(new_name, old_name)
                    is_comment = True
        result = super(IrModelFields, self).write(vals)

        for record in self:
            if 'name' in vals and is_comment:
                record.uncomment_field_view()

        return result

    def unlink(self):
        for record in self:
            record.remove_field_view()

        return super(IrModelFields, self).unlink()

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
        action_names = [f"ir.actions.act_window,{a.id}" for a in actions]

        return {
            'type': 'ir.actions.act_window',
            'name': 'Menus',
            'res_model': 'ir.ui.menu',
            'view_mode': 'list,form',
            'domain': [('action', 'in', action_names)],
            'context': {'default_action': action_names[0] if action_names else False},
        }

class CustomApp(models.Model):
    _name = 'erp.custom.app'
    _description = 'Custom App'

    name = fields.Char(string='Name')
    description = fields.Text(string='Description')

    model_ids = fields.One2many(
        'ir.model',
        'from_app_id',
        string='Models'
    )
    @api.model_create_multi
    def create(self, vals_list):

        result =  super(CustomApp, self).create(vals_list)

        for record in result:
            record.init_module()

        return result

    def unlink(self):
        for record in self:
            record.remove_module()

        return super(CustomApp, self).unlink()

    def init_module(self):
        current_file = os.path.abspath(__file__)

        models_dir = os.path.dirname(current_file)
        erp_dir = os.path.dirname(models_dir)
        addons_dir = os.path.dirname(erp_dir)
        new_folder = os.path.join(addons_dir, self.name)
        init_file_path = os.path.join(new_folder, '__init__.py')
        manifest_file_path = os.path.join(new_folder, '__manifest__.py')
        os.makedirs(new_folder, exist_ok=True)

        with open(init_file_path, 'w', encoding='utf-8') as f:
            f.write("""
def post_init_hook(env):
    pass

def uninstall_hook(env):
    pass
""")

        with open(manifest_file_path, 'w', encoding='utf-8') as f:
            f.write(f"""{{
    "name": "{self.description}",
    "version": "1.0",
    "author": "{self.env.user.name}",
    "summary": "{self.description}",
    "depends": ["mail", "base_automation"],
    "application": True,
    "post_init_hook": "post_init_hook",
}}""")

        return True

    def update_module(self):
        raise ValidationError("Module removal not implemented 22222.")
    
    def remove_module(self):
        raise ValidationError("Module removal not implemented yet.")

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

        self.create_menu(self.model_description, self.model_name, self.parent_menu_id.id)

    def delete_model(self):
        actions = self.env["ir.actions.act_window"].search([('res_model', '=', self.model_id.model)])
        for action in actions:
            menus = self.env['ir.ui.menu'].search([('action', '=', f"ir.actions.act_window,{action.id}")])
            menus.unlink()
            action.unlink()
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
        one2many = lambda s: s.ttype == "one2many"
        field_ids = self.model_id.field_id.filtered(lambda f: f.state == 'manual').sorted(key=lambda self: self.sequence)
        return field_ids.filtered(lambda s: not one2many(s)), field_ids.filtered(one2many)

    def update_list_view(self):
        normal_field_ids, one2many_fields = self.get_custom_fields()

        root = ET.Element("list")

        for field in normal_field_ids:
            ET.SubElement(root, "field", {
                "name": field.name,
                "optional": "show"
            })

        for field in one2many_fields:
            ET.SubElement(root, "field", {
                "name": field.name,
                "widget": "many2many_tags",
                "optional": "show"
            })
        
        ET.indent(root, space="    ")
        new_xml = ET.tostring(root, encoding="unicode")
        self.arch_base = new_xml

    def update_form_view(self):
        normal_field_ids, one2many_fields = self.get_custom_fields()
        field_ids = normal_field_ids.filtered(lambda f: not f.approval_field)
        approval_fields = normal_field_ids.filtered(lambda f: f.approval_field)

        form = ET.Element("form")

        # header
        header = ET.SubElement(form, "header")
        for field in approval_fields:
            ET.SubElement(header, "field", {
                "name": field.name,
                "widget": "statusbar",
                "options": "{'clickable': 1}"
            })

        # sheet
        sheet = ET.SubElement(form, "sheet")

        # group
        group = ET.SubElement(sheet, "group")
        for field in field_ids:
            ET.SubElement(group, "field", {
                "name": field.name
            })

        # notebook
        notebook = ET.SubElement(sheet, "notebook")
        for field in one2many_fields:
            page = ET.SubElement(notebook, "page", {
                "string": field.field_description,
                "name": field.name
            })
            ET.SubElement(page, "field", {
                "name": field.name
            })

        # chatter
        ET.SubElement(form, "chatter")

        ET.indent(form, space="    ")
        new_xml = ET.tostring(form, encoding="unicode")


        self.arch_base = new_xml

    def update_search_view(self):
        normal_field_ids, one2many_fields = self.get_custom_fields()

        root = ET.Element("search")

        for field in normal_field_ids:
            ET.SubElement(root, "field", {
                "name": field.name
            })
        
        ET.indent(root, space="    ")
        new_xml = ET.tostring(root, encoding="unicode")
        self.arch_base = new_xml
