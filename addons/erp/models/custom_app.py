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
        if not os.path.exists(manifest_file_path):
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
        return manifest_file_path

    def create_or_get_folder(self):
        new_folder = self.get_folder_path()
        os.makedirs(new_folder, exist_ok=True)
        self.create_or_get_manifest(new_folder)
        return new_folder

    def update_module(self):
        model_strs = ""
        for model in self.model_ids:
            model_strs += model.transfer_to_python_str()
        new_folder = self.create_or_get_folder()
        init_file_path = os.path.join(new_folder, '__init__.py')
        with open(init_file_path, 'w', encoding='utf-8') as f:
            f.write(f"""
def post_init_hook(env):
    custom_module_id = False
    if 'erp.custom.app' in env:
        custom_module_id = env['erp.custom.app'].create({{
            "name": "{self.name}",
            "description": "{self.description}",
        }})
    {model_strs}

def uninstall_hook(env):
    pass
""")

    def remove_module(self):
        # folder = self.get_folder_path()

        # if os.path.exists(folder):
        #     shutil.rmtree(folder)
        build = self.env['erp.build']
        for model in self.model_ids:
            build.delete_model(model)
