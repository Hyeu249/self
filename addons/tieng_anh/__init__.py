
    
from odoo.exceptions import ValidationError
from markupsafe import Markup

def post_init_hook(env):
    custom_module_id = False
    if 'nosheet.custom.app' in env:
        module_vals = {'name': 'Tiếng anh', 'description': 'Tiếng anh', 'uuid': 'uuid_096611a6ff2b4fd380726c652e6b7fb8'}
        custom_module_id = env['nosheet.custom.app'].create(module_vals)

    
    fields_payloads = []
    views_payloads = []
    def create_models():

        #model Câu hỏi
        model_vals = {'name': 'Câu hỏi', 'model': 'x_4dd43955387441ca862eb870c653ef4e', 'state': 'manual', 'transient': False, 'is_filter_manual': True, 'is_mail_thread': True, 'is_mail_activity': True}
        model_vals['from_app_id'] = custom_module_id.id if custom_module_id else False
        model_id = env['ir.model'].create(model_vals)
        x_name = env['ir.model.fields'].search([('model_id', '=', model_id.id), ('name', '=', 'x_name')], limit=1)
        if x_name:
            x_name.unlink()
        
        #model access right

        access_vals = {'name': 'Quyền cơ bản', 'perm_read': True, 'perm_write': True, 'perm_create': True, 'perm_unlink': True}
        group_id = env['res.groups'].search([('name', '=', 'Role / User')], limit=1)
        if not group_id:
            raise ValidationError('Group Role / User not found, please create it first.')

        access_vals['group_id'] = group_id.id
        access_vals['model_id'] = model_id.id
        env['ir.model.access'].create(access_vals)

        
        #model rules

        
        #model menus

        action_group_ids = []

        action_vals = {'name': 'Câu hỏi', 'name_id': 'Câu hỏi', 'res_model': 'x_4dd43955387441ca862eb870c653ef4e', 'type': 'ir.actions.act_window', 'usage': False, 'target': 'current', 'cache': True, 'view_mode': 'list,form', 'mobile_view_mode': 'kanban', 'domain': False, 'context': '{}', 'limit': 80, 'filter': False, 'help': "<p class='o_view_nocontent_smiling_face'>Create new document</p>"}
        action_vals['group_ids'] = [(6, 0, action_group_ids)]
        action_id = env['ir.actions.act_window'].create(action_vals)

        filter_user_ids = []

        user_id = env['res.users'].search([('name', '=', 'Administrator')], limit=1)
        if not user_id:
            raise ValidationError('User Administrator not found, please create it first.')
        else:
            filter_user_ids.append(user_id.id)

        filter_vals = {'name': 'Câu hỏi', 'model_id': 'x_4dd43955387441ca862eb870c653ef4e', 'is_default': True, 'domain': '[]', 'context': "{'group_by': ['x_de_tieng_anh']}", 'sort': '[]'}
        filter_vals['action_id'] = action_id.id if action_id else False
        filter_vals['user_ids'] = [(6, 0, filter_user_ids)]
        env['ir.filters'].create(filter_vals)

        menu_group_ids = []

        group_143_ids = []

        menu_domain = [('name', '=', 'Tiếng anh'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Tiếng anh', 'sequence': 10, 'group_ids': [(6, 0, group_143_ids)], 'is_custom': True}
        if False:
            menu_domain.append(('parent_id', '=', False.id))
            menu_create_domain['parent_id'] = False.id
        menu_143 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_143:
            menu_143 = env['ir.ui.menu'].create(menu_create_domain)

        menu_vals = {'name': 'Câu hỏi', 'sequence': 10, 'is_custom': True}
        menu_vals['action'] = f"ir.actions.act_window,{action_id.id}"
        menu_vals['group_ids'] = [(6, 0, menu_group_ids)]
        menu_vals['parent_id'] = menu_143.id if menu_143 else False
        env['ir.ui.menu'].create(menu_vals)

        
        #model views

        view_group_ids = []

        view_vals = {'name': 'x_4dd43955387441ca862eb870c653ef4e.form', 'model': 'x_4dd43955387441ca862eb870c653ef4e', 'arch_base': '<form>\n    <header/>\n    <sheet>\n        <div class="oe_title">\n            <h1>\n                <field name="x_name"/>\n            </h1>\n        </div>\n        <group>\n            <field name="x_progress" widget="progressbar"/>\n            <field name="x_vi_sao" invisible="not x_la_dung"/>\n        </group>\n        <notebook>\n            <page string="Câu trả lời" name="x_items">\n                <field name="x_items"/>\n            </page>\n            <page string="Info" name="info">\n                <group>\n                    <field name="x_stt"/>\n                    <field name="x_dap_an"/>\n                    <field name="x_de_tieng_anh"/>\n                    <field name="x_la_dung"/>\n                </group>\n            </page>\n        </notebook>\n    </sheet>\n    <chatter/>\n</form>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'form'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_4dd43955387441ca862eb870c653ef4e.list', 'model': 'x_4dd43955387441ca862eb870c653ef4e', 'arch_base': '<list>\n    <field name="x_stt" optional="show"/>\n    <field name="x_progress" optional="show"/>\n    <field name="x_name" optional="show"/>\n    <field name="x_vi_sao" optional="show"/>\n    <field name="x_dap_an" optional="show"/>\n    <field name="x_de_tieng_anh" optional="show"/>\n    <field name="x_la_dung" optional="show"/>\n    <field name="x_items" widget="many2many_tags" optional="show"/>\n</list>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'list'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_4dd43955387441ca862eb870c653ef4e.search', 'model': 'x_4dd43955387441ca862eb870c653ef4e', 'arch_base': '<search>\n    <field name="x_stt"/>\n    <field name="x_progress"/>\n    <field name="x_name"/>\n    <field name="x_vi_sao"/>\n    <field name="x_dap_an"/>\n    <field name="x_de_tieng_anh"/>\n    <field name="x_la_dung"/>\n</search>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'search'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)


        #prepare fields for model Câu hỏi

        groups = []
        field_vals = {'name': 'x_dap_an', 'field_description': 'Đáp án', 'ttype': 'char', 'help': False, 'sequence': 7, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': 'x_items', 'compute': "for record in self:\n    record['x_dap_an'] = record.x_items.filtered(lambda e: e.x_lua_chon).x_name\n", 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': False, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_de_tieng_anh', 'field_description': 'Đề tiếng anh', 'ttype': 'many2one', 'help': False, 'sequence': 8, 'relation': 'x_ef94afa6b5134f0b8dd945e90a6579d0', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_items', 'field_description': 'Items', 'ttype': 'one2many', 'help': False, 'sequence': 10, 'relation': 'x_adeff82d580544cab7d70678b2beb3e2', 'relation_field': 'x_cau_hoi', 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': False, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_la_dung', 'field_description': 'Là đúng', 'ttype': 'boolean', 'help': False, 'sequence': 9, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': 'x_items', 'compute': "\nfor record in self:\n    items = record.x_items.filtered(lambda e: e.x_la_dap_an and e.x_lua_chon)\n    record['x_la_dung'] = len(items) > 0\n", 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': False, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_name', 'field_description': 'Name', 'ttype': 'text', 'help': False, 'sequence': 5, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_progress', 'field_description': 'Progress', 'ttype': 'float', 'help': False, 'sequence': 4, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': 'x_de_tieng_anh.x_progress', 'depends': False, 'compute': False, 'required': False, 'readonly': True, 'invisible': False, 'store': True, 'index': False, 'copied': False, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_stt', 'field_description': 'STT', 'ttype': 'integer', 'help': False, 'sequence': 3, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_vi_sao', 'field_description': 'Vì sao', 'ttype': 'text', 'help': False, 'sequence': 6, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        #model Câu trả lời
        model_vals = {'name': 'Câu trả lời', 'model': 'x_adeff82d580544cab7d70678b2beb3e2', 'state': 'manual', 'transient': False, 'is_filter_manual': True, 'is_mail_thread': True, 'is_mail_activity': True}
        model_vals['from_app_id'] = custom_module_id.id if custom_module_id else False
        model_id = env['ir.model'].create(model_vals)
        x_name = env['ir.model.fields'].search([('model_id', '=', model_id.id), ('name', '=', 'x_name')], limit=1)
        if x_name:
            x_name.unlink()
        
        #model access right

        access_vals = {'name': 'Quyền cơ bản', 'perm_read': True, 'perm_write': True, 'perm_create': True, 'perm_unlink': True}
        group_id = env['res.groups'].search([('name', '=', 'Role / User')], limit=1)
        if not group_id:
            raise ValidationError('Group Role / User not found, please create it first.')

        access_vals['group_id'] = group_id.id
        access_vals['model_id'] = model_id.id
        env['ir.model.access'].create(access_vals)

        
        #model rules

        
        #model menus

        action_group_ids = []

        action_vals = {'name': 'Câu trả lời', 'name_id': 'Câu trả lời', 'res_model': 'x_adeff82d580544cab7d70678b2beb3e2', 'type': 'ir.actions.act_window', 'usage': False, 'target': 'current', 'cache': True, 'view_mode': 'list,form', 'mobile_view_mode': 'kanban', 'domain': False, 'context': '{}', 'limit': 80, 'filter': False, 'help': "<p class='o_view_nocontent_smiling_face'>Create new document</p>"}
        action_vals['group_ids'] = [(6, 0, action_group_ids)]
        action_id = env['ir.actions.act_window'].create(action_vals)

        menu_group_ids = []

        group_143_ids = []

        menu_domain = [('name', '=', 'Tiếng anh'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Tiếng anh', 'sequence': 10, 'group_ids': [(6, 0, group_143_ids)], 'is_custom': True}
        if False:
            menu_domain.append(('parent_id', '=', False.id))
            menu_create_domain['parent_id'] = False.id
        menu_143 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_143:
            menu_143 = env['ir.ui.menu'].create(menu_create_domain)

        menu_vals = {'name': 'Câu trả lời', 'sequence': 10, 'is_custom': True}
        menu_vals['action'] = f"ir.actions.act_window,{action_id.id}"
        menu_vals['group_ids'] = [(6, 0, menu_group_ids)]
        menu_vals['parent_id'] = menu_143.id if menu_143 else False
        env['ir.ui.menu'].create(menu_vals)

        
        #model views

        view_group_ids = []

        view_vals = {'name': 'x_adeff82d580544cab7d70678b2beb3e2.form', 'model': 'x_adeff82d580544cab7d70678b2beb3e2', 'arch_base': '<form>\n    <header/>\n    <sheet>\n        <group>\n            <field name="x_name"/>\n            <field name="x_cau_hoi" invisible="1"/>\n            <field name="x_la_dap_an"/>\n            <field name="x_lua_chon" invisible="1"/>\n        </group>\n        <notebook/>\n    </sheet>\n    <chatter/>\n</form>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'form'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_adeff82d580544cab7d70678b2beb3e2.list', 'model': 'x_adeff82d580544cab7d70678b2beb3e2', 'arch_base': '<list>\n    <field name="x_name" optional="show"/>\n    <field name="x_cau_hoi" optional="show"/>\n    <field name="x_la_dap_an" optional="show" widget="boolean_toggle"/>\n    <field name="x_lua_chon" optional="show" widget="boolean_toggle"/>\n</list>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'list'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_adeff82d580544cab7d70678b2beb3e2.search', 'model': 'x_adeff82d580544cab7d70678b2beb3e2', 'arch_base': '<search>\n    <field name="x_name"/>\n    <field name="x_cau_hoi"/>\n    <field name="x_la_dap_an"/>\n    <field name="x_lua_chon"/>\n</search>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'search'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)


        #prepare fields for model Câu trả lời

        groups = []
        field_vals = {'name': 'x_cau_hoi', 'field_description': 'Câu hỏi', 'ttype': 'many2one', 'help': False, 'sequence': 2, 'relation': 'x_4dd43955387441ca862eb870c653ef4e', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_la_dap_an', 'field_description': 'Là đáp án', 'ttype': 'boolean', 'help': False, 'sequence': 3, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_lua_chon', 'field_description': 'Lựa chọn', 'ttype': 'boolean', 'help': False, 'sequence': 4, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_name', 'field_description': 'Name', 'ttype': 'char', 'help': False, 'sequence': 1, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        #model Đề tiếng anh
        model_vals = {'name': 'Đề tiếng anh', 'model': 'x_ef94afa6b5134f0b8dd945e90a6579d0', 'state': 'manual', 'transient': False, 'is_filter_manual': True, 'is_mail_thread': True, 'is_mail_activity': True}
        model_vals['from_app_id'] = custom_module_id.id if custom_module_id else False
        model_id = env['ir.model'].create(model_vals)
        x_name = env['ir.model.fields'].search([('model_id', '=', model_id.id), ('name', '=', 'x_name')], limit=1)
        if x_name:
            x_name.unlink()
        
        #model access right

        access_vals = {'name': 'Quyền cơ bản', 'perm_read': True, 'perm_write': True, 'perm_create': True, 'perm_unlink': True}
        group_id = env['res.groups'].search([('name', '=', 'Role / User')], limit=1)
        if not group_id:
            raise ValidationError('Group Role / User not found, please create it first.')

        access_vals['group_id'] = group_id.id
        access_vals['model_id'] = model_id.id
        env['ir.model.access'].create(access_vals)

        
        #model rules

        
        #model menus

        action_group_ids = []

        action_vals = {'name': 'Đề tiếng anh', 'name_id': 'Đề tiếng anh', 'res_model': 'x_ef94afa6b5134f0b8dd945e90a6579d0', 'type': 'ir.actions.act_window', 'usage': False, 'target': 'current', 'cache': True, 'view_mode': 'list,form', 'mobile_view_mode': 'kanban', 'domain': False, 'context': '{}', 'limit': 80, 'filter': False, 'help': "<p class='o_view_nocontent_smiling_face'>Create new document</p>"}
        action_vals['group_ids'] = [(6, 0, action_group_ids)]
        action_id = env['ir.actions.act_window'].create(action_vals)

        menu_group_ids = []

        group_143_ids = []

        menu_domain = [('name', '=', 'Tiếng anh'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Tiếng anh', 'sequence': 10, 'group_ids': [(6, 0, group_143_ids)], 'is_custom': True}
        if False:
            menu_domain.append(('parent_id', '=', False.id))
            menu_create_domain['parent_id'] = False.id
        menu_143 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_143:
            menu_143 = env['ir.ui.menu'].create(menu_create_domain)

        menu_vals = {'name': 'Đề tiếng anh', 'sequence': 10, 'is_custom': True}
        menu_vals['action'] = f"ir.actions.act_window,{action_id.id}"
        menu_vals['group_ids'] = [(6, 0, menu_group_ids)]
        menu_vals['parent_id'] = menu_143.id if menu_143 else False
        env['ir.ui.menu'].create(menu_vals)

        
        #model views

        view_group_ids = []

        view_vals = {'name': 'x_ef94afa6b5134f0b8dd945e90a6579d0.form', 'model': 'x_ef94afa6b5134f0b8dd945e90a6579d0', 'arch_base': '<form>\n    <header/>\n    <sheet>\n        <div class="oe_title">\n            <h1>\n                <field name="x_name"/>\n            </h1>\n        </div>\n        <group>\n            <field name="x_progress" widget="progressbar"/>\n            <field name="x_description"/>\n        </group>\n        <notebook>\n            <page string="Câu hỏi" name="x_items">\n                <field name="x_items"/>\n            </page>\n        </notebook>\n    </sheet>\n    <chatter/>\n</form>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'form'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_ef94afa6b5134f0b8dd945e90a6579d0.list', 'model': 'x_ef94afa6b5134f0b8dd945e90a6579d0', 'arch_base': '<list>\n    <field name="x_name" optional="show"/>\n    <field name="x_description" optional="show"/>\n    <field name="x_progress" optional="show"/>\n    <field name="x_items" widget="many2many_tags" optional="show"/>\n</list>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'list'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_ef94afa6b5134f0b8dd945e90a6579d0.search', 'model': 'x_ef94afa6b5134f0b8dd945e90a6579d0', 'arch_base': '<search>\n    <field name="x_name"/>\n    <field name="x_description"/>\n    <field name="x_progress"/>\n</search>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'search'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)


        #prepare fields for model Đề tiếng anh

        groups = []
        field_vals = {'name': 'x_description', 'field_description': 'Description', 'ttype': 'text', 'help': False, 'sequence': 2, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_items', 'field_description': 'Items', 'ttype': 'one2many', 'help': False, 'sequence': 3, 'relation': 'x_4dd43955387441ca862eb870c653ef4e', 'relation_field': 'x_de_tieng_anh', 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': False, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_name', 'field_description': 'Name', 'ttype': 'char', 'help': False, 'sequence': 1, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_progress', 'field_description': 'Progress', 'ttype': 'float', 'help': False, 'sequence': 4, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': 'x_items', 'compute': "for record in self:\n    done = len(record.x_items.x_items.filtered(lambda e: e.x_dap_an and e.x_lua_chon))\n    total = len(record.x_items)\n    if total:\n        record['x_progress'] = done / total * 100\n    else:\n        record['x_progress'] = 0\n", 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': False, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

    create_models()

    
    #create fields for all models
    update_fields = []
    fields = sorted(
        fields_payloads,
        key=lambda f: bool(f['related'] or f['depends'] or f['ttype'] == 'one2many' or f['ttype'] == 'many2many')
    )
    for field in fields:
        selection_vals = field.pop('selection_vals', False)
        groups_vals = field.pop('groups_vals', False)
        related = field.pop('related', False)
        depends = field.pop('depends', False)
        compute = field.pop('compute', False)

        if field['relation']:
            t_model = env['ir.model'].search([('model', '=', field['relation'])], limit=1)
            field['selected_model_id'] = t_model.id if t_model else False

            if field['relation_field']:
                t_field = env['ir.model.fields'].search([('model', '=', field['relation']), ('name', '=', field['relation_field'])], limit=1)
                field['selected_field_id'] = t_field.id if t_field else False

        field_id = env['ir.model.fields'].create(field)
        if related or depends or compute:
            update_fields.append({
                'id': field_id.id,
                'related': related,
                'depends': depends,
                'compute': compute,
            })
        for selection in selection_vals:
            temp_vals = selection.copy()
            temp_vals['field_id'] = field_id.id
            if field['ttype'] == 'reference':
                t_model = env['ir.model'].search([('model', '=', temp_vals['value'])], limit=1)
                temp_vals['selected_model_id'] = t_model.id if t_model else False
            env['ir.model.fields.selection'].create(temp_vals)
        field_id.groups = [(6, 0, groups_vals)]
    for field in update_fields:
        field_id = env['ir.model.fields'].browse(field['id'])
        field_id.write({
            'related': field['related'],
            'depends': field['depends'],
            'compute': field['compute'],
        })

    
    for view in views_payloads:
        env['ir.ui.view'].create(view)

    
    #models automation

    model_id = env['ir.model'].search([('model', '=', 'x_4dd43955387441ca862eb870c653ef4e')])

    model_id = env['ir.model'].search([('model', '=', 'x_adeff82d580544cab7d70678b2beb3e2')])

    model_id = env['ir.model'].search([('model', '=', 'x_ef94afa6b5134f0b8dd945e90a6579d0')])

    action_group_ids = []

    sequence_id = False

    action_vals = {'name': 'Làm mới đáp án', 'sequence': 5, 'state': 'code', 'code': 'for record in records:\n    record.x_items.x_items.write({"x_lua_chon": False})', 'evaluation_type': 'value', 'update_path': False, 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'False'), ('model', '=', 'False')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)


def uninstall_hook(env):
    rec = env['nosheet.custom.app'].search([('uuid', '=', 'uuid_096611a6ff2b4fd380726c652e6b7fb8')], limit=1)

    if rec:
        rec.unlink()
