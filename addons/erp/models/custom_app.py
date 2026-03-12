from odoo import models, fields, api
from odoo.exceptions import ValidationError
import uuid
from odoo.fields import Command, Domain
import xml.etree.ElementTree as ET
import os
import unicodedata

def dash_text(text):
    text = unicodedata.normalize('NFD', text)
    text = "".join(c for c in text if unicodedata.category(c) != 'Mn')
    text = "_".join(text.split(" "))
    return text.lower().strip()

class CustomApp(models.Model):
    _name = 'erp.custom.app'
    _description = 'Custom App'

    _unique_name = models.Constraint(
        'UNIQUE(name)', 
        'This name is already registered!'
    )

    name = fields.Char(string='Name')
    description = fields.Text(string='Description')

    model_ids = fields.One2many(
        'ir.model',
        'from_app_id',
        string='Models'
    )
    menu_id = fields.Many2one(
        'ir.ui.menu',
        string='Menu',
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals["description"] = vals.get("description") or vals.get("name") or "No Description"

        result =  super(CustomApp, self).create(vals_list)

        for record in result:
            record.create_menu()

        return result

    def create_menu(self):
        menu_id = self.env["ir.ui.menu"].create(
            {
                "name": self.name,
                "is_custom": True,
            }
        )
        self.menu_id = menu_id.id

    def unlink(self):
        for record in self:
            record.remove_module()
            record.menu_id.unlink()

        return super(CustomApp, self).unlink()

    def get_folder_path(self):
        current_file = os.path.abspath(__file__)

        models_dir = os.path.dirname(current_file)
        erp_dir = os.path.dirname(models_dir)
        addons_dir = os.path.dirname(erp_dir)
        new_folder = os.path.join(addons_dir, dash_text(self.name))
        return new_folder

    def create_or_get_manifest(self, new_folder):
        manifest_file_path = os.path.join(new_folder, '__manifest__.py')
        with open(manifest_file_path, 'w', encoding='utf-8') as f:
            f.write(f"""{{
    "name": "{self.description}",
    "version": "1.0",
    "author": "{self.env.user.name}",
    "summary": "{self.description}",
    "depends": ["mail", "base_automation"],
    "application": True,
    "post_init_hook": "post_init_hook",
    "uninstall_hook": "uninstall_hook",
}}""")
        return manifest_file_path

    def create_or_get_folder(self):
        new_folder = self.get_folder_path()
        os.makedirs(new_folder, exist_ok=True)
        self.create_or_get_manifest(new_folder)
        return new_folder

    def create_module_py_str(self):
        strs = f'''
from odoo.exceptions import ValidationError

def post_init_hook(env):
    custom_module_id = False
    if 'erp.custom.app' in env:
        custom_module_id = env['{self._name}'].create({{
            "name": "{self.name}",
            "description": "{self.description}",
        }})
'''
        return strs

    def create_model_access_right_py_str(self, model_id):
        strs = ""
        model = self.env['ir.model'].browse(model_id)
        for access in model.access_ids:
            vals = access.read()[0]
            new_vals = {}
            for f in ['name', 'perm_read', 'perm_write', 'perm_create', 'perm_unlink']:
                new_vals[f] = vals.get(f)
            strs += f'''
        vals = {new_vals}
        group_id = env['{access.group_id._name}'].search([('name', '=', '{access.group_id.name}')], limit=1)
        if not group_id:
            raise ValidationError('Group {access.group_id.name} not found, please create it first.')

        vals['group_id'] = group_id.id
        vals['model_id'] = model_id.id
        env['{access._name}'].create(vals)
'''
        return strs

    def create_models_and_prepare_fields(self):
        strs = f'''
    payloads = []
    def create_models():
'''
        for model in self.model_ids:
            vals = model.read()[0]
            new_vals = {}
            for f in ['name', 'model', 'state', 'transient', 'is_filter_manual', 'is_mail_thread', 'is_mail_activity']:
                new_vals[f] = vals.get(f)
            strs += f'''
        #model {model.name}
        model_vals = {new_vals}
        model_vals['from_app_id'] = custom_module_id.id if custom_module_id else False
        model_id = env['ir.model'].create(model_vals)
        x_name = env['ir.model.fields'].search([('model_id', '=', model_id.id), ('name', '=', 'x_name')], limit=1)
        if x_name:
            x_name.unlink()
        {self.create_model_access_right_py_str(model.id)}
'''
            strs += f'''
        #prepare fields for model {model.name}
'''
            for field in model.field_id:
                vals = field.read()[0]
                new_vals = {}
                for f in ['name', 'field_description', 'ttype', 'help', 'sequence', 'relation', 'relation_field', 'relation_table', 'column1', 'column2', 'on_delete', 'domain', 'related', 'depends', 'compute', 'required', 'readonly', 'invisible', 'store', 'index', 'copied', 'tracking', 'approval_field']:
                    new_vals[f] = vals.get(f)
                strs += f'''
        groups = []
        field_vals = {new_vals}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []
'''
                for selection in field.selection_ids:
                    vals = selection.read()[0]
                    new_vals = {}
                    for f in ['sequence', 'value', 'name']:
                        new_vals[f] = vals.get(f)
                    strs += f'''
        field_vals['selection_vals'].append({new_vals})
'''
                for group in field.groups:
                    strs += f'''
        group_id = env['{group._name}'].search([('name', '=', '{group.name}')], limit=1)
        if not group_id:
            raise ValidationError('Group {group.name} not found, please create it first.')
        else:
            groups.append(group_id.id)
'''
                strs += f'''
        field_vals['groups_vals'] = groups
'''
                strs += '''
        payloads.append(field_vals)
'''
        strs += '''
    create_models()
'''
        return strs

    def create_fields(self):
        strs = f'''
    #create fields for all models
    fields = sorted(
        payloads,
        key=lambda f: bool(f['related'] or f['depends'] or f['ttype'] == 'one2many' or f['ttype'] == 'many2many')
    )
    for field in fields:
        selection_vals = field.pop('selection_vals', False)
        groups_vals = field.pop('groups_vals', False)
        field_id = env['ir.model.fields'].create(field)
        for selection in selection_vals:
            temp_vals = selection
            temp_vals['field_id'] = field_id.id
            env['ir.model.fields.selection'].create(temp_vals)
        field_id.groups = [(6, 0, groups_vals)]
'''
        return strs

    def update_module(self):
        model_strs = ""
        for model in self.model_ids:
            model_strs += model.transfer_to_python_str()
        new_folder = self.create_or_get_folder()
        init_file_path = os.path.join(new_folder, '__init__.py')
        with open(init_file_path, 'w', encoding='utf-8') as f:
            f.write(f"""
    {self.create_module_py_str()}
    {self.create_models_and_prepare_fields()}
    {self.create_fields()}

def uninstall_hook(env):
    rec = env['{self._name}'].search([('name', '=', '{self.name}')], limit=1)

    if rec:
        rec.unlink()
""")

    def remove_module(self):
        build = self.env['erp.build']
        for model in self.model_ids:
            build.delete_model(model)
