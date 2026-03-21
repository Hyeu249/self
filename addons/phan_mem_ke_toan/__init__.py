
    
from odoo.exceptions import ValidationError
from markupsafe import Markup

def post_init_hook(env):
    custom_module_id = False
    if 'erp.custom.app' in env:
        module_vals = {'name': 'Phần mềm kế toán', 'description': 'Phần mềm kế toán', 'uuid': 'uuid_ffa9efc5c0074f499c2e5e84dba64dd4'}
        custom_module_id = env['erp.custom.app'].create(module_vals)

    
    fields_payloads = []
    views_payloads = []
    def create_models():

        #model Bút toán điều chỉnh
        model_vals = {'name': 'Bút toán điều chỉnh', 'model': 'x_c81b7d76356048f2beaf302b92b63806', 'state': 'manual', 'transient': False, 'is_filter_manual': True, 'is_mail_thread': True, 'is_mail_activity': True}
        model_vals['from_app_id'] = custom_module_id.id if custom_module_id else False
        model_id = env['ir.model'].create(model_vals)
        x_name = env['ir.model.fields'].search([('model_id', '=', model_id.id), ('name', '=', 'x_name')], limit=1)
        if x_name:
            x_name.unlink()
        
        #model access right

        access_vals = {'name': 'access_x_c81b7d76356048f2beaf302b92b63806_user', 'perm_read': True, 'perm_write': True, 'perm_create': True, 'perm_unlink': True}
        group_id = env['res.groups'].search([('name', '=', 'Role / User')], limit=1)
        if not group_id:
            raise ValidationError('Group Role / User not found, please create it first.')

        access_vals['group_id'] = group_id.id
        access_vals['model_id'] = model_id.id
        env['ir.model.access'].create(access_vals)

        
        #model rules

        
        #model menus

        action_group_ids = []

        action_vals = {'name': 'Bút toán điều chỉnh', 'name_id': False, 'res_model': 'x_c81b7d76356048f2beaf302b92b63806', 'type': 'ir.actions.act_window', 'usage': False, 'target': 'current', 'cache': True, 'view_mode': 'list,form', 'mobile_view_mode': 'kanban', 'domain': False, 'context': '{}', 'limit': 80, 'filter': False, 'help': Markup('<p class="o_view_nocontent_smiling_face">Create new document</p>')}
        action_vals['group_ids'] = [(6, 0, action_group_ids)]
        action_id = env['ir.actions.act_window'].create(action_vals)

        menu_group_ids = []

        group_128_ids = []

        menu_domain = [('name', '=', 'Kế toán'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Kế toán', 'sequence': 11, 'group_ids': [(6, 0, group_128_ids)], 'is_custom': True}
        if False:
            menu_domain.append(('parent_id', '=', False.id))
            menu_create_domain['parent_id'] = False.id
        menu_128 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_128:
            menu_128 = env['ir.ui.menu'].create(menu_create_domain)

        menu_vals = {'name': 'Bút toán điều chỉnh', 'sequence': 3, 'is_custom': True}
        menu_vals['action'] = f"ir.actions.act_window,{action_id.id}"
        menu_vals['group_ids'] = [(6, 0, menu_group_ids)]
        menu_vals['parent_id'] = menu_128.id if menu_128 else False
        env['ir.ui.menu'].create(menu_vals)

        
        #model views

        view_group_ids = []

        view_vals = {'name': 'x_c81b7d76356048f2beaf302b92b63806.form', 'model': 'x_c81b7d76356048f2beaf302b92b63806', 'arch_base': '<form>\n    <header/>\n    <sheet>\n        <group>\n            <field name="x_name"/>\n            <field name="x_ngay_thang"/>\n            <field name="x_cong_ty_id"/>\n            <field name="x_ghi_chu"/>\n        </group>\n        <notebook>\n            <page string="Items" name="x_items">\n                <field name="x_items"/>\n            </page>\n        </notebook>\n    </sheet>\n    <chatter/>\n</form>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'form'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_c81b7d76356048f2beaf302b92b63806.list', 'model': 'x_c81b7d76356048f2beaf302b92b63806', 'arch_base': '<list>\n    <field name="x_name" optional="show"/>\n    <field name="x_ngay_thang" optional="show"/>\n    <field name="x_cong_ty_id" optional="show"/>\n    <field name="x_ghi_chu" optional="show"/>\n    <field name="x_items" widget="many2many_tags" optional="show"/>\n</list>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'list'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_c81b7d76356048f2beaf302b92b63806.search', 'model': 'x_c81b7d76356048f2beaf302b92b63806', 'arch_base': '<search>\n    <field name="x_name"/>\n    <field name="x_ngay_thang"/>\n    <field name="x_cong_ty_id"/>\n    <field name="x_ghi_chu"/>\n</search>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'search'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)


        #prepare fields for model Bút toán điều chỉnh

        groups = []
        field_vals = {'name': 'x_cong_ty_id', 'field_description': 'Công ty', 'ttype': 'many2one', 'help': False, 'sequence': 2, 'relation': 'x_1745d805e04a43b688d51b8267cc56fe', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_ghi_chu', 'field_description': 'Ghi chú', 'ttype': 'text', 'help': False, 'sequence': 3, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_items', 'field_description': 'Items', 'ttype': 'one2many', 'help': False, 'sequence': 4, 'relation': 'x_07c472ed342844baa780906b13dba020', 'relation_field': 'x_bt_dc_id', 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': False, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_name', 'field_description': 'Name', 'ttype': 'char', 'help': False, 'sequence': 0, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': True, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_ngay_thang', 'field_description': 'Ngày tháng', 'ttype': 'datetime', 'help': False, 'sequence': 1, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        #model Công ty
        model_vals = {'name': 'Công ty', 'model': 'x_1745d805e04a43b688d51b8267cc56fe', 'state': 'manual', 'transient': False, 'is_filter_manual': True, 'is_mail_thread': True, 'is_mail_activity': True}
        model_vals['from_app_id'] = custom_module_id.id if custom_module_id else False
        model_id = env['ir.model'].create(model_vals)
        x_name = env['ir.model.fields'].search([('model_id', '=', model_id.id), ('name', '=', 'x_name')], limit=1)
        if x_name:
            x_name.unlink()
        
        #model access right

        access_vals = {'name': 'access_x_1745d805e04a43b688d51b8267cc56fe_user', 'perm_read': True, 'perm_write': True, 'perm_create': True, 'perm_unlink': True}
        group_id = env['res.groups'].search([('name', '=', 'Role / User')], limit=1)
        if not group_id:
            raise ValidationError('Group Role / User not found, please create it first.')

        access_vals['group_id'] = group_id.id
        access_vals['model_id'] = model_id.id
        env['ir.model.access'].create(access_vals)

        
        #model rules

        
        #model menus

        action_group_ids = []

        action_vals = {'name': 'Công ty', 'name_id': False, 'res_model': 'x_1745d805e04a43b688d51b8267cc56fe', 'type': 'ir.actions.act_window', 'usage': False, 'target': 'current', 'cache': True, 'view_mode': 'list,form', 'mobile_view_mode': 'kanban', 'domain': False, 'context': '{}', 'limit': 80, 'filter': False, 'help': Markup('<p class="o_view_nocontent_smiling_face">Create new document</p>')}
        action_vals['group_ids'] = [(6, 0, action_group_ids)]
        action_id = env['ir.actions.act_window'].create(action_vals)

        menu_group_ids = []

        group_128_ids = []

        menu_domain = [('name', '=', 'Kế toán'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Kế toán', 'sequence': 11, 'group_ids': [(6, 0, group_128_ids)], 'is_custom': True}
        if False:
            menu_domain.append(('parent_id', '=', False.id))
            menu_create_domain['parent_id'] = False.id
        menu_128 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_128:
            menu_128 = env['ir.ui.menu'].create(menu_create_domain)

        menu_vals = {'name': 'Công ty', 'sequence': 10, 'is_custom': True}
        menu_vals['action'] = f"ir.actions.act_window,{action_id.id}"
        menu_vals['group_ids'] = [(6, 0, menu_group_ids)]
        menu_vals['parent_id'] = menu_128.id if menu_128 else False
        env['ir.ui.menu'].create(menu_vals)

        
        #model views

        view_group_ids = []

        view_vals = {'name': 'x_1745d805e04a43b688d51b8267cc56fe.form', 'model': 'x_1745d805e04a43b688d51b8267cc56fe', 'arch_base': '<form>\n    <header/>\n    <sheet>\n        <group string="Details">\n            <field name="x_name"/>\n            <field name="x_abbr"/>\n            <field name="x_tien_te_id"/>\n        </group>\n        <notebook>\n            <page string="Accounts">\n                <group>\n                    <group>\n                        <field name="x_tk_ngan_hang_id"/>\n                        <field name="x_tk_tien_mat_id"/>\n                        <field name="x_tk_phai_tra_id"/>\n                        <field name="x_tk_phai_thu_id"/>\n                    </group>\n                    <group>\n                        <field name="x_tk_chiet_khau_id"/>\n                        <field name="x_tk_chi_phi_id"/>\n                        <field name="x_tk_doanh_thu_id"/>\n                    </group>\n                </group>\n            </page>\n            <page string="Stock">\n                <group>\n                    <field name="x_tk_kho_id"/>\n                    <field name="x_tk_dieu_chinh_id"/>\n                    <field name="x_tk_hn_chua_hd_id"/>\n                </group>\n            </page>\n        </notebook>\n    </sheet>\n    <chatter/>\n</form>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'form'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_1745d805e04a43b688d51b8267cc56fe.list', 'model': 'x_1745d805e04a43b688d51b8267cc56fe', 'arch_base': '<list>\n    <field name="x_name" optional="show"/>\n    <field name="x_abbr" optional="show"/>\n    <field name="x_tien_te_id" optional="show"/>\n    <field name="x_tk_ngan_hang_id" optional="show"/>\n    <field name="x_tk_tien_mat_id" optional="show"/>\n    <field name="x_tk_phai_thu_id" optional="show"/>\n    <field name="x_tk_phai_tra_id" optional="show"/>\n    <field name="x_tk_chi_phi_id" optional="show"/>\n    <field name="x_tk_doanh_thu_id" optional="show"/>\n    <field name="x_tk_chiet_khau_id" optional="show"/>\n    <field name="x_tk_kho_id" optional="show"/>\n    <field name="x_tk_dieu_chinh_id" optional="show"/>\n    <field name="x_tk_hn_chua_hd_id" optional="show"/>\n</list>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'list'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_1745d805e04a43b688d51b8267cc56fe.search', 'model': 'x_1745d805e04a43b688d51b8267cc56fe', 'arch_base': '<search>\n    <field name="x_name"/>\n    <field name="x_abbr"/>\n    <field name="x_tien_te_id"/>\n    <field name="x_tk_ngan_hang_id"/>\n    <field name="x_tk_tien_mat_id"/>\n    <field name="x_tk_phai_thu_id"/>\n    <field name="x_tk_phai_tra_id"/>\n    <field name="x_tk_chi_phi_id"/>\n    <field name="x_tk_doanh_thu_id"/>\n    <field name="x_tk_chiet_khau_id"/>\n    <field name="x_tk_kho_id"/>\n    <field name="x_tk_dieu_chinh_id"/>\n    <field name="x_tk_hn_chua_hd_id"/>\n</search>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'search'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)


        #prepare fields for model Công ty

        groups = []
        field_vals = {'name': 'x_abbr', 'field_description': 'Abbr', 'ttype': 'char', 'help': False, 'sequence': 1, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_name', 'field_description': 'Name', 'ttype': 'char', 'help': False, 'sequence': 0, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_tien_te_id', 'field_description': 'Tiền tệ', 'ttype': 'many2one', 'help': False, 'sequence': 2, 'relation': 'res.currency', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_tk_chi_phi_id', 'field_description': 'Tài khoản chi phí', 'ttype': 'many2one', 'help': False, 'sequence': 7, 'relation': 'x_500b7a5ea68541cb82fc5cc4e7be7c6a', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[("x_is_group", "=", False)]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_tk_chiet_khau_id', 'field_description': 'Tài khoản chiết khấu', 'ttype': 'many2one', 'help': False, 'sequence': 9, 'relation': 'x_500b7a5ea68541cb82fc5cc4e7be7c6a', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[("x_is_group", "=", False)]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_tk_dieu_chinh_id', 'field_description': 'Tài khoản điều chỉnh', 'ttype': 'many2one', 'help': False, 'sequence': 11, 'relation': 'x_500b7a5ea68541cb82fc5cc4e7be7c6a', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[("x_is_group", "=", False)]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_tk_doanh_thu_id', 'field_description': 'Tài khoản doanh thu', 'ttype': 'many2one', 'help': False, 'sequence': 8, 'relation': 'x_500b7a5ea68541cb82fc5cc4e7be7c6a', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[("x_is_group", "=", False)]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_tk_hn_chua_hd_id', 'field_description': 'Tài khoản HN. chưa HĐ', 'ttype': 'many2one', 'help': False, 'sequence': 12, 'relation': 'x_500b7a5ea68541cb82fc5cc4e7be7c6a', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[("x_is_group", "=", False)]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_tk_kho_id', 'field_description': 'Tài khoản kho', 'ttype': 'many2one', 'help': False, 'sequence': 10, 'relation': 'x_500b7a5ea68541cb82fc5cc4e7be7c6a', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[("x_is_group", "=", False)]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_tk_ngan_hang_id', 'field_description': 'Tài khoản ngân hàng', 'ttype': 'many2one', 'help': False, 'sequence': 3, 'relation': 'x_500b7a5ea68541cb82fc5cc4e7be7c6a', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[("x_is_group", "=", False)]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_tk_phai_thu_id', 'field_description': 'Tài khoản phải thu', 'ttype': 'many2one', 'help': False, 'sequence': 5, 'relation': 'x_500b7a5ea68541cb82fc5cc4e7be7c6a', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[("x_is_group", "=", False)]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_tk_phai_tra_id', 'field_description': 'Tài khoản phải trả', 'ttype': 'many2one', 'help': False, 'sequence': 6, 'relation': 'x_500b7a5ea68541cb82fc5cc4e7be7c6a', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[("x_is_group", "=", False)]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_tk_tien_mat_id', 'field_description': 'Tài khoản tiền mặt', 'ttype': 'many2one', 'help': False, 'sequence': 4, 'relation': 'x_500b7a5ea68541cb82fc5cc4e7be7c6a', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[("x_is_group", "=", False)]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        #model Danh sách giá
        model_vals = {'name': 'Danh sách giá', 'model': 'x_7007229d76ad42cd853707f65fd26e33', 'state': 'manual', 'transient': False, 'is_filter_manual': True, 'is_mail_thread': True, 'is_mail_activity': True}
        model_vals['from_app_id'] = custom_module_id.id if custom_module_id else False
        model_id = env['ir.model'].create(model_vals)
        x_name = env['ir.model.fields'].search([('model_id', '=', model_id.id), ('name', '=', 'x_name')], limit=1)
        if x_name:
            x_name.unlink()
        
        #model access right

        access_vals = {'name': 'access_x_7007229d76ad42cd853707f65fd26e33_user', 'perm_read': True, 'perm_write': True, 'perm_create': True, 'perm_unlink': True}
        group_id = env['res.groups'].search([('name', '=', 'Role / User')], limit=1)
        if not group_id:
            raise ValidationError('Group Role / User not found, please create it first.')

        access_vals['group_id'] = group_id.id
        access_vals['model_id'] = model_id.id
        env['ir.model.access'].create(access_vals)

        
        #model rules

        
        #model menus

        action_group_ids = []

        action_vals = {'name': 'Danh sách giá', 'name_id': False, 'res_model': 'x_7007229d76ad42cd853707f65fd26e33', 'type': 'ir.actions.act_window', 'usage': False, 'target': 'current', 'cache': True, 'view_mode': 'list,form', 'mobile_view_mode': 'kanban', 'domain': False, 'context': '{}', 'limit': 80, 'filter': False, 'help': Markup('<p class="o_view_nocontent_smiling_face">Create new document</p>')}
        action_vals['group_ids'] = [(6, 0, action_group_ids)]
        action_id = env['ir.actions.act_window'].create(action_vals)

        menu_group_ids = []

        group_132_ids = []

        group_131_ids = []

        menu_domain = [('name', '=', 'Bán hàng'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Bán hàng', 'sequence': 9, 'group_ids': [(6, 0, group_131_ids)], 'is_custom': True}
        if False:
            menu_domain.append(('parent_id', '=', False.id))
            menu_create_domain['parent_id'] = False.id
        menu_131 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_131:
            menu_131 = env['ir.ui.menu'].create(menu_create_domain)

        menu_domain = [('name', '=', 'Giá khách hàng'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Giá khách hàng', 'sequence': 10, 'group_ids': [(6, 0, group_132_ids)], 'is_custom': True}
        if menu_131:
            menu_domain.append(('parent_id', '=', menu_131.id))
            menu_create_domain['parent_id'] = menu_131.id
        menu_132 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_132:
            menu_132 = env['ir.ui.menu'].create(menu_create_domain)

        menu_vals = {'name': 'Danh sách giá', 'sequence': 10, 'is_custom': True}
        menu_vals['action'] = f"ir.actions.act_window,{action_id.id}"
        menu_vals['group_ids'] = [(6, 0, menu_group_ids)]
        menu_vals['parent_id'] = menu_132.id if menu_132 else False
        env['ir.ui.menu'].create(menu_vals)

        
        #model views

        view_group_ids = []

        view_vals = {'name': 'x_7007229d76ad42cd853707f65fd26e33.form', 'model': 'x_7007229d76ad42cd853707f65fd26e33', 'arch_base': '<form>\n    <header/>\n    <sheet>\n        <group>\n            <field name="x_name"/>\n        </group>\n        <notebook>\n            <page string="Giá hàng hoá" name="x_ghh_id">\n                <field name="x_ghh_id"/>\n            </page>\n        </notebook>\n    </sheet>\n    <chatter/>\n</form>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'form'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_7007229d76ad42cd853707f65fd26e33.list', 'model': 'x_7007229d76ad42cd853707f65fd26e33', 'arch_base': '<list>\n    <field name="x_name" optional="show"/>\n    <field name="x_ghh_id" widget="many2many_tags" optional="show"/>\n</list>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'list'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_7007229d76ad42cd853707f65fd26e33.search', 'model': 'x_7007229d76ad42cd853707f65fd26e33', 'arch_base': '<search>\n    <field name="x_name"/>\n</search>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'search'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)


        #prepare fields for model Danh sách giá

        groups = []
        field_vals = {'name': 'x_ghh_id', 'field_description': 'Giá hàng hoá', 'ttype': 'one2many', 'help': False, 'sequence': 1, 'relation': 'x_291da0ecd8dc4491b65b085a6adbb09a', 'relation_field': 'x_dsg_id', 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': False, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_name', 'field_description': 'Name', 'ttype': 'char', 'help': False, 'sequence': 0, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        #model Giá hàng hoá
        model_vals = {'name': 'Giá hàng hoá', 'model': 'x_291da0ecd8dc4491b65b085a6adbb09a', 'state': 'manual', 'transient': False, 'is_filter_manual': True, 'is_mail_thread': True, 'is_mail_activity': True}
        model_vals['from_app_id'] = custom_module_id.id if custom_module_id else False
        model_id = env['ir.model'].create(model_vals)
        x_name = env['ir.model.fields'].search([('model_id', '=', model_id.id), ('name', '=', 'x_name')], limit=1)
        if x_name:
            x_name.unlink()
        
        #model access right

        access_vals = {'name': 'access_x_291da0ecd8dc4491b65b085a6adbb09a_user', 'perm_read': True, 'perm_write': True, 'perm_create': True, 'perm_unlink': True}
        group_id = env['res.groups'].search([('name', '=', 'Role / User')], limit=1)
        if not group_id:
            raise ValidationError('Group Role / User not found, please create it first.')

        access_vals['group_id'] = group_id.id
        access_vals['model_id'] = model_id.id
        env['ir.model.access'].create(access_vals)

        
        #model rules

        
        #model menus

        action_group_ids = []

        action_vals = {'name': 'Giá hàng hoá', 'name_id': False, 'res_model': 'x_291da0ecd8dc4491b65b085a6adbb09a', 'type': 'ir.actions.act_window', 'usage': False, 'target': 'current', 'cache': True, 'view_mode': 'list,form', 'mobile_view_mode': 'kanban', 'domain': False, 'context': '{}', 'limit': 80, 'filter': False, 'help': Markup('<p class="o_view_nocontent_smiling_face">Create new document</p>')}
        action_vals['group_ids'] = [(6, 0, action_group_ids)]
        action_id = env['ir.actions.act_window'].create(action_vals)

        menu_group_ids = []

        group_132_ids = []

        group_131_ids = []

        menu_domain = [('name', '=', 'Bán hàng'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Bán hàng', 'sequence': 9, 'group_ids': [(6, 0, group_131_ids)], 'is_custom': True}
        if False:
            menu_domain.append(('parent_id', '=', False.id))
            menu_create_domain['parent_id'] = False.id
        menu_131 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_131:
            menu_131 = env['ir.ui.menu'].create(menu_create_domain)

        menu_domain = [('name', '=', 'Giá khách hàng'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Giá khách hàng', 'sequence': 10, 'group_ids': [(6, 0, group_132_ids)], 'is_custom': True}
        if menu_131:
            menu_domain.append(('parent_id', '=', menu_131.id))
            menu_create_domain['parent_id'] = menu_131.id
        menu_132 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_132:
            menu_132 = env['ir.ui.menu'].create(menu_create_domain)

        menu_vals = {'name': 'Giá hàng hoá', 'sequence': 10, 'is_custom': True}
        menu_vals['action'] = f"ir.actions.act_window,{action_id.id}"
        menu_vals['group_ids'] = [(6, 0, menu_group_ids)]
        menu_vals['parent_id'] = menu_132.id if menu_132 else False
        env['ir.ui.menu'].create(menu_vals)

        
        #model views

        view_group_ids = []

        view_vals = {'name': 'x_291da0ecd8dc4491b65b085a6adbb09a.form', 'model': 'x_291da0ecd8dc4491b65b085a6adbb09a', 'arch_base': '<form>\n    <header/>\n    <sheet>\n        <group>\n            <field name="x_name"/>\n            <field name="x_hang_hoa_id"/>\n            <field name="x_dsg_id"/>\n        </group>\n        <notebook>\n            <page string="Items" name="x_items">\n                <field name="x_items"/>\n            </page>\n        </notebook>\n    </sheet>\n    <chatter/>\n</form>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'form'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_291da0ecd8dc4491b65b085a6adbb09a.list', 'model': 'x_291da0ecd8dc4491b65b085a6adbb09a', 'arch_base': '<list>\n    <field name="x_name" optional="show"/>\n    <field name="x_hang_hoa_id" optional="show"/>\n    <field name="x_dsg_id" optional="show"/>\n    <field name="x_items" widget="many2many_tags" optional="show"/>\n</list>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'list'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_291da0ecd8dc4491b65b085a6adbb09a.search', 'model': 'x_291da0ecd8dc4491b65b085a6adbb09a', 'arch_base': '<search>\n    <field name="x_name"/>\n    <field name="x_hang_hoa_id"/>\n    <field name="x_dsg_id"/>\n</search>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'search'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)


        #prepare fields for model Giá hàng hoá

        groups = []
        field_vals = {'name': 'x_dsg_id', 'field_description': 'Danh sách giá', 'ttype': 'many2one', 'help': False, 'sequence': 3, 'relation': 'x_7007229d76ad42cd853707f65fd26e33', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_hang_hoa_id', 'field_description': 'Tên hàng hoá', 'ttype': 'many2one', 'help': False, 'sequence': 1, 'relation': 'x_9e57e8e385ca48d1b28e1cf1d646b8b6', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_items', 'field_description': 'Items', 'ttype': 'one2many', 'help': False, 'sequence': 2, 'relation': 'x_2f04e2bc228d49b5b8c910eadba9b63c', 'relation_field': 'x_ghh_id', 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': False, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_name', 'field_description': 'Name', 'ttype': 'char', 'help': False, 'sequence': 0, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': True, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        #model Giá áp dụng
        model_vals = {'name': 'Giá áp dụng', 'model': 'x_2f04e2bc228d49b5b8c910eadba9b63c', 'state': 'manual', 'transient': False, 'is_filter_manual': True, 'is_mail_thread': True, 'is_mail_activity': True}
        model_vals['from_app_id'] = custom_module_id.id if custom_module_id else False
        model_id = env['ir.model'].create(model_vals)
        x_name = env['ir.model.fields'].search([('model_id', '=', model_id.id), ('name', '=', 'x_name')], limit=1)
        if x_name:
            x_name.unlink()
        
        #model access right

        access_vals = {'name': 'access_x_2f04e2bc228d49b5b8c910eadba9b63c_user', 'perm_read': True, 'perm_write': True, 'perm_create': True, 'perm_unlink': True}
        group_id = env['res.groups'].search([('name', '=', 'Role / User')], limit=1)
        if not group_id:
            raise ValidationError('Group Role / User not found, please create it first.')

        access_vals['group_id'] = group_id.id
        access_vals['model_id'] = model_id.id
        env['ir.model.access'].create(access_vals)

        
        #model rules

        
        #model menus

        action_group_ids = []

        action_vals = {'name': 'Giá áp dụng', 'name_id': False, 'res_model': 'x_2f04e2bc228d49b5b8c910eadba9b63c', 'type': 'ir.actions.act_window', 'usage': False, 'target': 'current', 'cache': True, 'view_mode': 'list,form', 'mobile_view_mode': 'kanban', 'domain': False, 'context': '{}', 'limit': 80, 'filter': False, 'help': Markup('<p class="o_view_nocontent_smiling_face">Create new document</p>')}
        action_vals['group_ids'] = [(6, 0, action_group_ids)]
        action_id = env['ir.actions.act_window'].create(action_vals)

        menu_group_ids = []

        group_132_ids = []

        group_131_ids = []

        menu_domain = [('name', '=', 'Bán hàng'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Bán hàng', 'sequence': 9, 'group_ids': [(6, 0, group_131_ids)], 'is_custom': True}
        if False:
            menu_domain.append(('parent_id', '=', False.id))
            menu_create_domain['parent_id'] = False.id
        menu_131 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_131:
            menu_131 = env['ir.ui.menu'].create(menu_create_domain)

        menu_domain = [('name', '=', 'Giá khách hàng'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Giá khách hàng', 'sequence': 10, 'group_ids': [(6, 0, group_132_ids)], 'is_custom': True}
        if menu_131:
            menu_domain.append(('parent_id', '=', menu_131.id))
            menu_create_domain['parent_id'] = menu_131.id
        menu_132 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_132:
            menu_132 = env['ir.ui.menu'].create(menu_create_domain)

        menu_vals = {'name': 'Giá áp dụng', 'sequence': 10, 'is_custom': True}
        menu_vals['action'] = f"ir.actions.act_window,{action_id.id}"
        menu_vals['group_ids'] = [(6, 0, menu_group_ids)]
        menu_vals['parent_id'] = menu_132.id if menu_132 else False
        env['ir.ui.menu'].create(menu_vals)

        
        #model views

        view_group_ids = []

        view_vals = {'name': 'x_2f04e2bc228d49b5b8c910eadba9b63c.form', 'model': 'x_2f04e2bc228d49b5b8c910eadba9b63c', 'arch_base': '<form>\n    <header/>\n    <sheet>\n        <group>\n            <field name="x_name"/>\n            <field name="x_tu_ngay"/>\n            <field name="x_den_ngay"/>\n            <field name="x_don_gia"/>\n            <field name="x_ghh_id"/>\n            <field name="x_hang_hoa_id"/>\n            <field name="x_dsg_id"/>\n        </group>\n        <notebook/>\n    </sheet>\n    <chatter/>\n</form>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'form'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_2f04e2bc228d49b5b8c910eadba9b63c.list', 'model': 'x_2f04e2bc228d49b5b8c910eadba9b63c', 'arch_base': '<list>\n    <field name="x_name" optional="show"/>\n    <field name="x_tu_ngay" optional="show"/>\n    <field name="x_den_ngay" optional="show"/>\n    <field name="x_don_gia" optional="show"/>\n    <field name="x_ghh_id" optional="show"/>\n    <field name="x_hang_hoa_id" optional="show"/>\n    <field name="x_dsg_id" optional="show"/>\n</list>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'list'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_2f04e2bc228d49b5b8c910eadba9b63c.search', 'model': 'x_2f04e2bc228d49b5b8c910eadba9b63c', 'arch_base': '<search>\n    <field name="x_name"/>\n    <field name="x_tu_ngay"/>\n    <field name="x_den_ngay"/>\n    <field name="x_don_gia"/>\n    <field name="x_ghh_id"/>\n    <field name="x_hang_hoa_id"/>\n    <field name="x_dsg_id"/>\n</search>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'search'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)


        #prepare fields for model Giá áp dụng

        groups = []
        field_vals = {'name': 'x_den_ngay', 'field_description': 'Đến ngày', 'ttype': 'date', 'help': False, 'sequence': 2, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_don_gia', 'field_description': 'Đơn giá', 'ttype': 'float', 'help': False, 'sequence': 3, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_dsg_id', 'field_description': 'Danh sách giá', 'ttype': 'many2one', 'help': False, 'sequence': 6, 'relation': 'x_7007229d76ad42cd853707f65fd26e33', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': 'x_ghh_id.x_dsg_id', 'depends': False, 'compute': False, 'required': False, 'readonly': True, 'invisible': False, 'store': True, 'index': False, 'copied': False, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_ghh_id', 'field_description': 'Giá hàng hoá', 'ttype': 'many2one', 'help': False, 'sequence': 4, 'relation': 'x_291da0ecd8dc4491b65b085a6adbb09a', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_hang_hoa_id', 'field_description': 'Hàng hoá', 'ttype': 'many2one', 'help': False, 'sequence': 5, 'relation': 'x_9e57e8e385ca48d1b28e1cf1d646b8b6', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': 'x_ghh_id.x_hang_hoa_id', 'depends': False, 'compute': False, 'required': False, 'readonly': True, 'invisible': False, 'store': True, 'index': False, 'copied': False, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_name', 'field_description': 'Name', 'ttype': 'char', 'help': False, 'sequence': 0, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': True, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_tu_ngay', 'field_description': 'Từ ngày', 'ttype': 'date', 'help': False, 'sequence': 1, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        #model Hoá đơn
        model_vals = {'name': 'Hoá đơn', 'model': 'x_df3b7908507d42b2ac2b3a78d2660696', 'state': 'manual', 'transient': False, 'is_filter_manual': True, 'is_mail_thread': True, 'is_mail_activity': True}
        model_vals['from_app_id'] = custom_module_id.id if custom_module_id else False
        model_id = env['ir.model'].create(model_vals)
        x_name = env['ir.model.fields'].search([('model_id', '=', model_id.id), ('name', '=', 'x_name')], limit=1)
        if x_name:
            x_name.unlink()
        
        #model access right

        access_vals = {'name': 'access_x_df3b7908507d42b2ac2b3a78d2660696_user', 'perm_read': True, 'perm_write': True, 'perm_create': True, 'perm_unlink': True}
        group_id = env['res.groups'].search([('name', '=', 'Role / User')], limit=1)
        if not group_id:
            raise ValidationError('Group Role / User not found, please create it first.')

        access_vals['group_id'] = group_id.id
        access_vals['model_id'] = model_id.id
        env['ir.model.access'].create(access_vals)

        
        #model rules

        
        #model menus

        action_group_ids = []

        action_vals = {'name': 'Hoá đơn', 'name_id': False, 'res_model': 'x_df3b7908507d42b2ac2b3a78d2660696', 'type': 'ir.actions.act_window', 'usage': False, 'target': 'current', 'cache': True, 'view_mode': 'list,form', 'mobile_view_mode': 'kanban', 'domain': False, 'context': '{}', 'limit': 80, 'filter': False, 'help': Markup('<p class="o_view_nocontent_smiling_face">Create new document</p>')}
        action_vals['group_ids'] = [(6, 0, action_group_ids)]
        action_id = env['ir.actions.act_window'].create(action_vals)

        menu_group_ids = []

        group_131_ids = []

        menu_domain = [('name', '=', 'Bán hàng'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Bán hàng', 'sequence': 9, 'group_ids': [(6, 0, group_131_ids)], 'is_custom': True}
        if False:
            menu_domain.append(('parent_id', '=', False.id))
            menu_create_domain['parent_id'] = False.id
        menu_131 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_131:
            menu_131 = env['ir.ui.menu'].create(menu_create_domain)

        menu_vals = {'name': 'Hoá đơn', 'sequence': 10, 'is_custom': True}
        menu_vals['action'] = f"ir.actions.act_window,{action_id.id}"
        menu_vals['group_ids'] = [(6, 0, menu_group_ids)]
        menu_vals['parent_id'] = menu_131.id if menu_131 else False
        env['ir.ui.menu'].create(menu_vals)

        
        #model views

        view_group_ids = []

        view_vals = {'name': 'x_df3b7908507d42b2ac2b3a78d2660696.form', 'model': 'x_df3b7908507d42b2ac2b3a78d2660696', 'arch_base': '<form>\n                        <sheet>\n                        <group>\n                            <field name="x_name"/>\n                        </group>\n                        </sheet>\n                        <chatter/>\n                    </form>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'form'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_df3b7908507d42b2ac2b3a78d2660696.list', 'model': 'x_df3b7908507d42b2ac2b3a78d2660696', 'arch_base': '<list>\n                        <field name="x_name"/>\n                    </list>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'list'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_df3b7908507d42b2ac2b3a78d2660696.search', 'model': 'x_df3b7908507d42b2ac2b3a78d2660696', 'arch_base': '<search><field name="x_name"/></search>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'search'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)


        #prepare fields for model Hoá đơn

        groups = []
        field_vals = {'name': 'x_name', 'field_description': 'Name', 'ttype': 'char', 'help': False, 'sequence': 0, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': True, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        #model Hàng hoá
        model_vals = {'name': 'Hàng hoá', 'model': 'x_9e57e8e385ca48d1b28e1cf1d646b8b6', 'state': 'manual', 'transient': False, 'is_filter_manual': True, 'is_mail_thread': True, 'is_mail_activity': True}
        model_vals['from_app_id'] = custom_module_id.id if custom_module_id else False
        model_id = env['ir.model'].create(model_vals)
        x_name = env['ir.model.fields'].search([('model_id', '=', model_id.id), ('name', '=', 'x_name')], limit=1)
        if x_name:
            x_name.unlink()
        
        #model access right

        access_vals = {'name': 'access_x_9e57e8e385ca48d1b28e1cf1d646b8b6_user', 'perm_read': True, 'perm_write': True, 'perm_create': True, 'perm_unlink': True}
        group_id = env['res.groups'].search([('name', '=', 'Role / User')], limit=1)
        if not group_id:
            raise ValidationError('Group Role / User not found, please create it first.')

        access_vals['group_id'] = group_id.id
        access_vals['model_id'] = model_id.id
        env['ir.model.access'].create(access_vals)

        
        #model rules

        
        #model menus

        action_group_ids = []

        action_vals = {'name': 'Hàng hoá', 'name_id': False, 'res_model': 'x_9e57e8e385ca48d1b28e1cf1d646b8b6', 'type': 'ir.actions.act_window', 'usage': False, 'target': 'current', 'cache': True, 'view_mode': 'list,form', 'mobile_view_mode': 'kanban', 'domain': False, 'context': '{}', 'limit': 80, 'filter': False, 'help': Markup('<p class="o_view_nocontent_smiling_face">Create new document</p>')}
        action_vals['group_ids'] = [(6, 0, action_group_ids)]
        action_id = env['ir.actions.act_window'].create(action_vals)

        menu_group_ids = []

        group_137_ids = []

        menu_domain = [('name', '=', 'Quản lý kho'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Quản lý kho', 'sequence': 10, 'group_ids': [(6, 0, group_137_ids)], 'is_custom': True}
        if False:
            menu_domain.append(('parent_id', '=', False.id))
            menu_create_domain['parent_id'] = False.id
        menu_137 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_137:
            menu_137 = env['ir.ui.menu'].create(menu_create_domain)

        menu_vals = {'name': 'Hàng hoá', 'sequence': 1, 'is_custom': True}
        menu_vals['action'] = f"ir.actions.act_window,{action_id.id}"
        menu_vals['group_ids'] = [(6, 0, menu_group_ids)]
        menu_vals['parent_id'] = menu_137.id if menu_137 else False
        env['ir.ui.menu'].create(menu_vals)

        menu_group_ids = []

        group_131_ids = []

        menu_domain = [('name', '=', 'Bán hàng'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Bán hàng', 'sequence': 9, 'group_ids': [(6, 0, group_131_ids)], 'is_custom': True}
        if False:
            menu_domain.append(('parent_id', '=', False.id))
            menu_create_domain['parent_id'] = False.id
        menu_131 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_131:
            menu_131 = env['ir.ui.menu'].create(menu_create_domain)

        menu_vals = {'name': 'Hàng hoá', 'sequence': 1, 'is_custom': True}
        menu_vals['action'] = f"ir.actions.act_window,{action_id.id}"
        menu_vals['group_ids'] = [(6, 0, menu_group_ids)]
        menu_vals['parent_id'] = menu_131.id if menu_131 else False
        env['ir.ui.menu'].create(menu_vals)

        
        #model views

        view_group_ids = []

        view_vals = {'name': 'x_9e57e8e385ca48d1b28e1cf1d646b8b6.form', 'model': 'x_9e57e8e385ca48d1b28e1cf1d646b8b6', 'arch_base': '<form>\n    <header/>\n    <sheet>\n        <group>\n            <field name="x_name"/>\n            <field name="x_gia_von"/>\n        </group>\n        <notebook/>\n    </sheet>\n    <chatter/>\n</form>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'form'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_9e57e8e385ca48d1b28e1cf1d646b8b6.list', 'model': 'x_9e57e8e385ca48d1b28e1cf1d646b8b6', 'arch_base': '<list editable="bottom">\n    <field name="x_name" optional="show"/>\n    <field name="x_gia_von" optional="show"/>\n</list>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'list'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_9e57e8e385ca48d1b28e1cf1d646b8b6.search', 'model': 'x_9e57e8e385ca48d1b28e1cf1d646b8b6', 'arch_base': '<search>\n    <field name="x_name"/>\n    <field name="x_gia_von"/>\n</search>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'search'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)


        #prepare fields for model Hàng hoá

        groups = []
        field_vals = {'name': 'x_gia_von', 'field_description': 'Giá vốn', 'ttype': 'float', 'help': False, 'sequence': 1, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_name', 'field_description': 'Name', 'ttype': 'char', 'help': False, 'sequence': 0, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        #model HĐ mua bán
        model_vals = {'name': 'HĐ mua bán', 'model': 'x_3719e3f84afb4332a727a7a10419d8f7', 'state': 'manual', 'transient': False, 'is_filter_manual': True, 'is_mail_thread': True, 'is_mail_activity': True}
        model_vals['from_app_id'] = custom_module_id.id if custom_module_id else False
        model_id = env['ir.model'].create(model_vals)
        x_name = env['ir.model.fields'].search([('model_id', '=', model_id.id), ('name', '=', 'x_name')], limit=1)
        if x_name:
            x_name.unlink()
        
        #model access right

        access_vals = {'name': 'access_x_3719e3f84afb4332a727a7a10419d8f7_user', 'perm_read': True, 'perm_write': True, 'perm_create': True, 'perm_unlink': True}
        group_id = env['res.groups'].search([('name', '=', 'Role / User')], limit=1)
        if not group_id:
            raise ValidationError('Group Role / User not found, please create it first.')

        access_vals['group_id'] = group_id.id
        access_vals['model_id'] = model_id.id
        env['ir.model.access'].create(access_vals)

        
        #model rules

        
        #model menus

        action_group_ids = []

        action_vals = {'name': 'HĐ mua bán', 'name_id': False, 'res_model': 'x_3719e3f84afb4332a727a7a10419d8f7', 'type': 'ir.actions.act_window', 'usage': False, 'target': 'current', 'cache': True, 'view_mode': 'list,form', 'mobile_view_mode': 'kanban', 'domain': False, 'context': '{}', 'limit': 80, 'filter': False, 'help': Markup('<p class="o_view_nocontent_smiling_face">Create new document</p>')}
        action_vals['group_ids'] = [(6, 0, action_group_ids)]
        action_id = env['ir.actions.act_window'].create(action_vals)

        menu_group_ids = []

        group_131_ids = []

        menu_domain = [('name', '=', 'Bán hàng'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Bán hàng', 'sequence': 9, 'group_ids': [(6, 0, group_131_ids)], 'is_custom': True}
        if False:
            menu_domain.append(('parent_id', '=', False.id))
            menu_create_domain['parent_id'] = False.id
        menu_131 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_131:
            menu_131 = env['ir.ui.menu'].create(menu_create_domain)

        menu_vals = {'name': 'HĐ mua bán', 'sequence': 3, 'is_custom': True}
        menu_vals['action'] = f"ir.actions.act_window,{action_id.id}"
        menu_vals['group_ids'] = [(6, 0, menu_group_ids)]
        menu_vals['parent_id'] = menu_131.id if menu_131 else False
        env['ir.ui.menu'].create(menu_vals)

        
        #model views

        view_group_ids = []

        view_vals = {'name': 'x_3719e3f84afb4332a727a7a10419d8f7.form', 'model': 'x_3719e3f84afb4332a727a7a10419d8f7', 'arch_base': '<form>\n    <header/>\n    <sheet>\n        <group>\n            <field name="x_name"/>\n            <field name="x_ngay_thang"/>\n            <field name="x_dai_ly_id"/>\n            <field name="x_kho_hang_id"/>\n            <field name="x_cong_ty_id"/>\n        </group>\n        <notebook>\n            <page string="Mua bán hàng hoá" name="x_items" invisible="context.get(\'is_hide\', False)">\n                <field name="x_items"/>\n            </page>\n        </notebook>\n    </sheet>\n    <chatter/>\n</form>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'form'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_3719e3f84afb4332a727a7a10419d8f7.list', 'model': 'x_3719e3f84afb4332a727a7a10419d8f7', 'arch_base': '<list>\n    <field name="x_name" optional="show"/>\n    <field name="x_ngay_thang" optional="show"/>\n    <field name="x_dai_ly_id" optional="show"/>\n    <field name="x_kho_hang_id" optional="show"/>\n    <field name="x_cong_ty_id" optional="show"/>\n    <field name="x_items" widget="many2many_tags" optional="show"/>\n</list>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'list'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_3719e3f84afb4332a727a7a10419d8f7.search', 'model': 'x_3719e3f84afb4332a727a7a10419d8f7', 'arch_base': '<search>\n    <field name="x_name"/>\n    <field name="x_ngay_thang"/>\n    <field name="x_dai_ly_id"/>\n    <field name="x_kho_hang_id"/>\n    <field name="x_cong_ty_id"/>\n</search>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'search'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)


        #prepare fields for model HĐ mua bán

        groups = []
        field_vals = {'name': 'x_cong_ty_id', 'field_description': 'Công ty', 'ttype': 'many2one', 'help': False, 'sequence': 4, 'relation': 'x_1745d805e04a43b688d51b8267cc56fe', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_dai_ly_id', 'field_description': 'NCC/KH', 'ttype': 'many2one', 'help': False, 'sequence': 2, 'relation': 'x_47586e8c7d9744c3a1f1992a10a30b16', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_items', 'field_description': 'Mua bán hàng hoá', 'ttype': 'one2many', 'help': False, 'sequence': 5, 'relation': 'x_77605823c2c743a19dfe7674cdbca3bd', 'relation_field': 'x_hd_id', 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': False, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_kho_hang_id', 'field_description': 'Kho hàng', 'ttype': 'many2one', 'help': False, 'sequence': 3, 'relation': 'x_48c748e1bb1047d3ad931c4535cc12cf', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_name', 'field_description': 'Name', 'ttype': 'char', 'help': False, 'sequence': 0, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': True, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_ngay_thang', 'field_description': 'Ngày tháng', 'ttype': 'datetime', 'help': False, 'sequence': 1, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        #model Kho hàng
        model_vals = {'name': 'Kho hàng', 'model': 'x_48c748e1bb1047d3ad931c4535cc12cf', 'state': 'manual', 'transient': False, 'is_filter_manual': True, 'is_mail_thread': True, 'is_mail_activity': True}
        model_vals['from_app_id'] = custom_module_id.id if custom_module_id else False
        model_id = env['ir.model'].create(model_vals)
        x_name = env['ir.model.fields'].search([('model_id', '=', model_id.id), ('name', '=', 'x_name')], limit=1)
        if x_name:
            x_name.unlink()
        
        #model access right

        access_vals = {'name': 'access_x_48c748e1bb1047d3ad931c4535cc12cf_user', 'perm_read': True, 'perm_write': True, 'perm_create': True, 'perm_unlink': True}
        group_id = env['res.groups'].search([('name', '=', 'Role / User')], limit=1)
        if not group_id:
            raise ValidationError('Group Role / User not found, please create it first.')

        access_vals['group_id'] = group_id.id
        access_vals['model_id'] = model_id.id
        env['ir.model.access'].create(access_vals)

        
        #model rules

        
        #model menus

        action_group_ids = []

        action_vals = {'name': 'Kho hàng', 'name_id': False, 'res_model': 'x_48c748e1bb1047d3ad931c4535cc12cf', 'type': 'ir.actions.act_window', 'usage': False, 'target': 'current', 'cache': True, 'view_mode': 'list,form', 'mobile_view_mode': 'kanban', 'domain': False, 'context': '{}', 'limit': 80, 'filter': False, 'help': Markup('<p class="o_view_nocontent_smiling_face">Create new document</p>')}
        action_vals['group_ids'] = [(6, 0, action_group_ids)]
        action_id = env['ir.actions.act_window'].create(action_vals)

        menu_group_ids = []

        group_137_ids = []

        menu_domain = [('name', '=', 'Quản lý kho'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Quản lý kho', 'sequence': 10, 'group_ids': [(6, 0, group_137_ids)], 'is_custom': True}
        if False:
            menu_domain.append(('parent_id', '=', False.id))
            menu_create_domain['parent_id'] = False.id
        menu_137 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_137:
            menu_137 = env['ir.ui.menu'].create(menu_create_domain)

        menu_vals = {'name': 'Kho hàng', 'sequence': 10, 'is_custom': True}
        menu_vals['action'] = f"ir.actions.act_window,{action_id.id}"
        menu_vals['group_ids'] = [(6, 0, menu_group_ids)]
        menu_vals['parent_id'] = menu_137.id if menu_137 else False
        env['ir.ui.menu'].create(menu_vals)

        
        #model views

        view_group_ids = []

        view_vals = {'name': 'x_48c748e1bb1047d3ad931c4535cc12cf.form', 'model': 'x_48c748e1bb1047d3ad931c4535cc12cf', 'arch_base': '<form>\n                        <sheet>\n                        <group>\n                            <field name="x_name"/>\n                        </group>\n                        </sheet>\n                        <chatter/>\n                    </form>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'form'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_48c748e1bb1047d3ad931c4535cc12cf.list', 'model': 'x_48c748e1bb1047d3ad931c4535cc12cf', 'arch_base': '<list>\n                        <field name="x_name"/>\n                    </list>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'list'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_48c748e1bb1047d3ad931c4535cc12cf.search', 'model': 'x_48c748e1bb1047d3ad931c4535cc12cf', 'arch_base': '<search><field name="x_name"/></search>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'search'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)


        #prepare fields for model Kho hàng

        groups = []
        field_vals = {'name': 'x_name', 'field_description': 'Name', 'ttype': 'char', 'help': False, 'sequence': 0, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        #model Mua bán hàng hoá
        model_vals = {'name': 'Mua bán hàng hoá', 'model': 'x_77605823c2c743a19dfe7674cdbca3bd', 'state': 'manual', 'transient': False, 'is_filter_manual': True, 'is_mail_thread': True, 'is_mail_activity': True}
        model_vals['from_app_id'] = custom_module_id.id if custom_module_id else False
        model_id = env['ir.model'].create(model_vals)
        x_name = env['ir.model.fields'].search([('model_id', '=', model_id.id), ('name', '=', 'x_name')], limit=1)
        if x_name:
            x_name.unlink()
        
        #model access right

        access_vals = {'name': 'access_x_77605823c2c743a19dfe7674cdbca3bd_user', 'perm_read': True, 'perm_write': True, 'perm_create': True, 'perm_unlink': True}
        group_id = env['res.groups'].search([('name', '=', 'Role / User')], limit=1)
        if not group_id:
            raise ValidationError('Group Role / User not found, please create it first.')

        access_vals['group_id'] = group_id.id
        access_vals['model_id'] = model_id.id
        env['ir.model.access'].create(access_vals)

        
        #model rules

        
        #model menus

        action_group_ids = []

        action_vals = {'name': 'Mua bán hàng hoá', 'name_id': False, 'res_model': 'x_77605823c2c743a19dfe7674cdbca3bd', 'type': 'ir.actions.act_window', 'usage': False, 'target': 'current', 'cache': True, 'view_mode': 'list,form', 'mobile_view_mode': 'kanban', 'domain': False, 'context': '{}', 'limit': 80, 'filter': False, 'help': Markup('<p class="o_view_nocontent_smiling_face">Create new document</p>')}
        action_vals['group_ids'] = [(6, 0, action_group_ids)]
        action_id = env['ir.actions.act_window'].create(action_vals)

        menu_group_ids = []

        group_131_ids = []

        menu_domain = [('name', '=', 'Bán hàng'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Bán hàng', 'sequence': 9, 'group_ids': [(6, 0, group_131_ids)], 'is_custom': True}
        if False:
            menu_domain.append(('parent_id', '=', False.id))
            menu_create_domain['parent_id'] = False.id
        menu_131 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_131:
            menu_131 = env['ir.ui.menu'].create(menu_create_domain)

        menu_vals = {'name': 'Mua bán hàng hoá', 'sequence': 2, 'is_custom': True}
        menu_vals['action'] = f"ir.actions.act_window,{action_id.id}"
        menu_vals['group_ids'] = [(6, 0, menu_group_ids)]
        menu_vals['parent_id'] = menu_131.id if menu_131 else False
        env['ir.ui.menu'].create(menu_vals)

        
        #model views

        view_group_ids = []

        view_vals = {'name': 'x_77605823c2c743a19dfe7674cdbca3bd.form', 'model': 'x_77605823c2c743a19dfe7674cdbca3bd', 'arch_base': '<form>\n    <header/>\n    <sheet>\n        <group>\n            <field name="x_name"/>\n            <field name="x_ngay_thang"/>\n            <field name="x_hd_id"/>\n            <field name="x_dai_ly_id"/>\n            <field name="x_hang_hoa_id"/>\n            <field name="x_muc_dich"/>\n            <field name="x_sl"/>\n            <field name="x_don_gia"/>\n            <field name="x_thanh_tien"/>\n            <field name="x_thanh_toan"/>\n            <field name="x_ghi_chu"/>\n            <field name="x_gia_von" readonly="1"/>\n            <field name="x_kho_hang_id"/>\n            <field name="x_cong_ty_id"/>\n        </group>\n        <notebook>\n            <page string="Nhật ký bán hàng" name="x_nk_tt_ids">\n                <field name="x_nk_tt_ids"/>\n            </page>\n        </notebook>\n    </sheet>\n    <chatter/>\n</form>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'form'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_77605823c2c743a19dfe7674cdbca3bd.list', 'model': 'x_77605823c2c743a19dfe7674cdbca3bd', 'arch_base': '<list editable="bottom" open_form_view="true">\n    <field name="x_name" optional="show"/>\n    <field name="x_ngay_thang" optional="show"/>\n    <field name="x_hd_id" optional="show" context="{\'is_hide\': not x_hd_id}"/>\n    <field name="x_dai_ly_id" optional="show"/>\n    <field name="x_hang_hoa_id" optional="show"/>\n    <field name="x_muc_dich" optional="show"/>\n    <field name="x_sl" optional="show"/>\n    <field name="x_don_gia" optional="show"/>\n    <field name="x_thanh_tien" optional="show" sum="Thành tiền"/>\n    <field name="x_thanh_toan" optional="show" sum="Thanh toán"/>\n    <field name="x_ghi_chu" optional="show"/>\n    <field name="x_gia_von" optional="show" readonly="1"/>\n    <field name="x_kho_hang_id" optional="show"/>\n    <field name="x_cong_ty_id" optional="show"/>\n</list>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'list'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_77605823c2c743a19dfe7674cdbca3bd.search', 'model': 'x_77605823c2c743a19dfe7674cdbca3bd', 'arch_base': '<search>\n    <field name="x_name"/>\n    <field name="x_ngay_thang"/>\n    <field name="x_hd_id"/>\n    <field name="x_dai_ly_id"/>\n    <field name="x_hang_hoa_id"/>\n    <field name="x_muc_dich"/>\n    <field name="x_sl"/>\n    <field name="x_don_gia"/>\n    <field name="x_thanh_tien"/>\n    <field name="x_thanh_toan"/>\n    <field name="x_ghi_chu"/>\n    <field name="x_gia_von"/>\n    <field name="x_kho_hang_id"/>\n    <field name="x_cong_ty_id"/>\n</search>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'search'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)


        #prepare fields for model Mua bán hàng hoá

        groups = []
        field_vals = {'name': 'x_cong_ty_id', 'field_description': 'Công ty', 'ttype': 'many2one', 'help': False, 'sequence': 13, 'relation': 'x_1745d805e04a43b688d51b8267cc56fe', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': 'x_hd_id.x_cong_ty_id', 'depends': False, 'compute': False, 'required': False, 'readonly': True, 'invisible': False, 'store': True, 'index': False, 'copied': False, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_dai_ly_id', 'field_description': 'KH/NCC', 'ttype': 'many2one', 'help': False, 'sequence': 3, 'relation': 'x_47586e8c7d9744c3a1f1992a10a30b16', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': 'x_hd_id.x_dai_ly_id', 'depends': False, 'compute': False, 'required': False, 'readonly': True, 'invisible': False, 'store': True, 'index': False, 'copied': False, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_don_gia', 'field_description': 'Đơn giá', 'ttype': 'float', 'help': False, 'sequence': 7, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_ghi_chu', 'field_description': 'Ghi chú', 'ttype': 'text', 'help': False, 'sequence': 10, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_gia_von', 'field_description': 'Giá vốn', 'ttype': 'float', 'help': False, 'sequence': 11, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_hang_hoa_id', 'field_description': 'Tên hàng hoá', 'ttype': 'many2one', 'help': False, 'sequence': 4, 'relation': 'x_9e57e8e385ca48d1b28e1cf1d646b8b6', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_hd_id', 'field_description': 'Số HĐ', 'ttype': 'many2one', 'help': False, 'sequence': 2, 'relation': 'x_3719e3f84afb4332a727a7a10419d8f7', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_kho_hang_id', 'field_description': 'Kho hàng', 'ttype': 'many2one', 'help': False, 'sequence': 12, 'relation': 'x_48c748e1bb1047d3ad931c4535cc12cf', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': 'x_hd_id.x_kho_hang_id', 'depends': False, 'compute': False, 'required': False, 'readonly': True, 'invisible': False, 'store': True, 'index': False, 'copied': False, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_muc_dich', 'field_description': 'Mục đích', 'ttype': 'selection', 'help': False, 'sequence': 5, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['selection_vals'].append({'sequence': 0, 'value': 'Nhập hàng', 'name': 'Nhập hàng'})

        field_vals['selection_vals'].append({'sequence': 1, 'value': 'Xuất hàng', 'name': 'Xuất hàng'})

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_name', 'field_description': 'Name', 'ttype': 'char', 'help': False, 'sequence': 0, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': True, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_ngay_thang', 'field_description': 'Ngày tháng', 'ttype': 'datetime', 'help': False, 'sequence': 1, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': 'x_hd_id.x_ngay_thang', 'depends': False, 'compute': False, 'required': False, 'readonly': True, 'invisible': False, 'store': True, 'index': False, 'copied': False, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_nk_tt_ids', 'field_description': 'Nhật ký thanh toán', 'ttype': 'one2many', 'help': False, 'sequence': 14, 'relation': 'x_7076d1049e954d7985d7e2cd445e5b20', 'relation_field': 'x_mbhh_id', 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': False, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_sl', 'field_description': 'Số lượng', 'ttype': 'float', 'help': False, 'sequence': 6, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_thanh_tien', 'field_description': 'Thành tiền', 'ttype': 'float', 'help': 'hello 2', 'sequence': 8, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': False, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_thanh_toan', 'field_description': 'Thanh toán', 'ttype': 'float', 'help': False, 'sequence': 9, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': True, 'invisible': False, 'store': False, 'index': False, 'copied': False, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        #model Nhật ký thanh toán
        model_vals = {'name': 'Nhật ký thanh toán', 'model': 'x_7076d1049e954d7985d7e2cd445e5b20', 'state': 'manual', 'transient': False, 'is_filter_manual': True, 'is_mail_thread': True, 'is_mail_activity': True}
        model_vals['from_app_id'] = custom_module_id.id if custom_module_id else False
        model_id = env['ir.model'].create(model_vals)
        x_name = env['ir.model.fields'].search([('model_id', '=', model_id.id), ('name', '=', 'x_name')], limit=1)
        if x_name:
            x_name.unlink()
        
        #model access right

        access_vals = {'name': 'access_x_7076d1049e954d7985d7e2cd445e5b20_user', 'perm_read': True, 'perm_write': True, 'perm_create': True, 'perm_unlink': True}
        group_id = env['res.groups'].search([('name', '=', 'Role / User')], limit=1)
        if not group_id:
            raise ValidationError('Group Role / User not found, please create it first.')

        access_vals['group_id'] = group_id.id
        access_vals['model_id'] = model_id.id
        env['ir.model.access'].create(access_vals)

        
        #model rules

        
        #model menus

        action_group_ids = []

        action_vals = {'name': 'Nhật ký thanh toán', 'name_id': False, 'res_model': 'x_7076d1049e954d7985d7e2cd445e5b20', 'type': 'ir.actions.act_window', 'usage': False, 'target': 'current', 'cache': True, 'view_mode': 'list,form', 'mobile_view_mode': 'kanban', 'domain': False, 'context': '{}', 'limit': 80, 'filter': False, 'help': Markup('<p class="o_view_nocontent_smiling_face">Create new document</p>')}
        action_vals['group_ids'] = [(6, 0, action_group_ids)]
        action_id = env['ir.actions.act_window'].create(action_vals)

        menu_group_ids = []

        group_131_ids = []

        menu_domain = [('name', '=', 'Bán hàng'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Bán hàng', 'sequence': 9, 'group_ids': [(6, 0, group_131_ids)], 'is_custom': True}
        if False:
            menu_domain.append(('parent_id', '=', False.id))
            menu_create_domain['parent_id'] = False.id
        menu_131 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_131:
            menu_131 = env['ir.ui.menu'].create(menu_create_domain)

        menu_vals = {'name': 'Nhật ký thanh toán', 'sequence': 4, 'is_custom': True}
        menu_vals['action'] = f"ir.actions.act_window,{action_id.id}"
        menu_vals['group_ids'] = [(6, 0, menu_group_ids)]
        menu_vals['parent_id'] = menu_131.id if menu_131 else False
        env['ir.ui.menu'].create(menu_vals)

        
        #model views

        view_group_ids = []

        view_vals = {'name': 'x_7076d1049e954d7985d7e2cd445e5b20.form', 'model': 'x_7076d1049e954d7985d7e2cd445e5b20', 'arch_base': '<form>\n    <header/>\n    <sheet>\n        <group>\n            <field name="x_name"/>\n            <field name="x_ngay_thang"/>\n            <field name="x_loai_thanh_toan"/>\n            <field name="x_thanh_toan"/>\n            <field name="x_mbhh_id"/>\n            <field name="x_hoa_don_id"/>\n            <field name="x_cong_ty_id"/>\n        </group>\n        <notebook/>\n    </sheet>\n    <chatter/>\n</form>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'form'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_7076d1049e954d7985d7e2cd445e5b20.list', 'model': 'x_7076d1049e954d7985d7e2cd445e5b20', 'arch_base': '<list editable="bottom">\n    <field name="x_name" optional="show"/>\n    <field name="x_ngay_thang" optional="show"/>\n    <field name="x_loai_thanh_toan" optional="show"/>\n    <field name="x_thanh_toan" optional="show"/>\n    <field name="x_mbhh_id" optional="show"/>\n    <field name="x_hoa_don_id" optional="show"/>\n    <field name="x_cong_ty_id" optional="show"/>\n</list>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'list'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_7076d1049e954d7985d7e2cd445e5b20.search', 'model': 'x_7076d1049e954d7985d7e2cd445e5b20', 'arch_base': '<search>\n    <field name="x_name"/>\n    <field name="x_ngay_thang"/>\n    <field name="x_loai_thanh_toan"/>\n    <field name="x_thanh_toan"/>\n    <field name="x_mbhh_id"/>\n    <field name="x_hoa_don_id"/>\n    <field name="x_cong_ty_id"/>\n</search>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'search'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)


        #prepare fields for model Nhật ký thanh toán

        groups = []
        field_vals = {'name': 'x_cong_ty_id', 'field_description': 'Công ty', 'ttype': 'many2one', 'help': False, 'sequence': 6, 'relation': 'x_1745d805e04a43b688d51b8267cc56fe', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': 'x_mbhh_id.x_cong_ty_id', 'depends': False, 'compute': False, 'required': False, 'readonly': True, 'invisible': False, 'store': True, 'index': False, 'copied': False, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_hoa_don_id', 'field_description': 'Hoá đơn', 'ttype': 'many2one', 'help': False, 'sequence': 5, 'relation': 'x_df3b7908507d42b2ac2b3a78d2660696', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_loai_thanh_toan', 'field_description': 'Loại thanh toán', 'ttype': 'selection', 'help': False, 'sequence': 2, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['selection_vals'].append({'sequence': 0, 'value': 'Tiền mặt', 'name': 'Tiền mặt'})

        field_vals['selection_vals'].append({'sequence': 1, 'value': 'Ngân hàng', 'name': 'Ngân hàng'})

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_mbhh_id', 'field_description': 'Mua bán hàng hoá', 'ttype': 'many2one', 'help': False, 'sequence': 4, 'relation': 'x_77605823c2c743a19dfe7674cdbca3bd', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_name', 'field_description': 'Name', 'ttype': 'char', 'help': False, 'sequence': 0, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': True, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_ngay_thang', 'field_description': 'Ngày tháng', 'ttype': 'datetime', 'help': False, 'sequence': 1, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_thanh_toan', 'field_description': 'Thanh toán', 'ttype': 'float', 'help': False, 'sequence': 3, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        #model Phiếu kho
        model_vals = {'name': 'Phiếu kho', 'model': 'x_c90f6c65498d4983bdf0d7371f40618b', 'state': 'manual', 'transient': False, 'is_filter_manual': True, 'is_mail_thread': True, 'is_mail_activity': True}
        model_vals['from_app_id'] = custom_module_id.id if custom_module_id else False
        model_id = env['ir.model'].create(model_vals)
        x_name = env['ir.model.fields'].search([('model_id', '=', model_id.id), ('name', '=', 'x_name')], limit=1)
        if x_name:
            x_name.unlink()
        
        #model access right

        access_vals = {'name': 'access_x_c90f6c65498d4983bdf0d7371f40618b_user', 'perm_read': True, 'perm_write': True, 'perm_create': True, 'perm_unlink': True}
        group_id = env['res.groups'].search([('name', '=', 'Role / User')], limit=1)
        if not group_id:
            raise ValidationError('Group Role / User not found, please create it first.')

        access_vals['group_id'] = group_id.id
        access_vals['model_id'] = model_id.id
        env['ir.model.access'].create(access_vals)

        
        #model rules

        
        #model menus

        action_group_ids = []

        action_vals = {'name': 'Phiếu kho', 'name_id': False, 'res_model': 'x_c90f6c65498d4983bdf0d7371f40618b', 'type': 'ir.actions.act_window', 'usage': False, 'target': 'current', 'cache': True, 'view_mode': 'list,form', 'mobile_view_mode': 'kanban', 'domain': False, 'context': '{}', 'limit': 80, 'filter': False, 'help': Markup('<p class="o_view_nocontent_smiling_face">Create new document</p>')}
        action_vals['group_ids'] = [(6, 0, action_group_ids)]
        action_id = env['ir.actions.act_window'].create(action_vals)

        menu_group_ids = []

        group_137_ids = []

        menu_domain = [('name', '=', 'Quản lý kho'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Quản lý kho', 'sequence': 10, 'group_ids': [(6, 0, group_137_ids)], 'is_custom': True}
        if False:
            menu_domain.append(('parent_id', '=', False.id))
            menu_create_domain['parent_id'] = False.id
        menu_137 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_137:
            menu_137 = env['ir.ui.menu'].create(menu_create_domain)

        menu_vals = {'name': 'Phiếu kho', 'sequence': 5, 'is_custom': True}
        menu_vals['action'] = f"ir.actions.act_window,{action_id.id}"
        menu_vals['group_ids'] = [(6, 0, menu_group_ids)]
        menu_vals['parent_id'] = menu_137.id if menu_137 else False
        env['ir.ui.menu'].create(menu_vals)

        
        #model views

        view_group_ids = []

        view_vals = {'name': 'x_c90f6c65498d4983bdf0d7371f40618b.form', 'model': 'x_c90f6c65498d4983bdf0d7371f40618b', 'arch_base': '<form>\n    <header/>\n    <sheet>\n        <group>\n            <field name="x_name"/>\n            <field name="x_ngay_thang"/>\n            <field name="x_kho_nguon_id"/>\n            <field name="x_kho_dich_id"/>\n            <field name="x_cong_ty_id"/>\n        </group>\n        <notebook>\n            <page string="Xuất nhập kho" name="x_items" invisible="context.get(\'is_hide\', False)">\n                <field name="x_items"/>\n            </page>\n        </notebook>\n    </sheet>\n    <chatter/>\n</form>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'form'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_c90f6c65498d4983bdf0d7371f40618b.list', 'model': 'x_c90f6c65498d4983bdf0d7371f40618b', 'arch_base': '<list>\n    <field name="x_name" optional="show"/>\n    <field name="x_ngay_thang" optional="show"/>\n    <field name="x_kho_nguon_id" optional="show"/>\n    <field name="x_kho_dich_id" optional="show"/>\n    <field name="x_cong_ty_id" optional="show"/>\n    <field name="x_items" widget="many2many_tags" optional="show"/>\n</list>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'list'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_c90f6c65498d4983bdf0d7371f40618b.search', 'model': 'x_c90f6c65498d4983bdf0d7371f40618b', 'arch_base': '<search>\n    <field name="x_name"/>\n    <field name="x_ngay_thang"/>\n    <field name="x_kho_nguon_id"/>\n    <field name="x_kho_dich_id"/>\n    <field name="x_cong_ty_id"/>\n</search>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'search'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)


        #prepare fields for model Phiếu kho

        groups = []
        field_vals = {'name': 'x_cong_ty_id', 'field_description': 'Công ty', 'ttype': 'many2one', 'help': False, 'sequence': 4, 'relation': 'x_1745d805e04a43b688d51b8267cc56fe', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_items', 'field_description': 'Xuất nhập kho', 'ttype': 'one2many', 'help': False, 'sequence': 5, 'relation': 'x_f0637b5ecea4413289b8fee8086af2e0', 'relation_field': 'x_phieu_kho_id', 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': False, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_kho_dich_id', 'field_description': 'Kho đích', 'ttype': 'many2one', 'help': False, 'sequence': 3, 'relation': 'x_48c748e1bb1047d3ad931c4535cc12cf', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_kho_nguon_id', 'field_description': 'Kho nguồn', 'ttype': 'many2one', 'help': False, 'sequence': 2, 'relation': 'x_48c748e1bb1047d3ad931c4535cc12cf', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_name', 'field_description': 'Name', 'ttype': 'char', 'help': False, 'sequence': 0, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': True, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_ngay_thang', 'field_description': 'Ngày tháng', 'ttype': 'datetime', 'help': False, 'sequence': 1, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        #model Sổ cái kho
        model_vals = {'name': 'Sổ cái kho', 'model': 'x_c68ffd06f8144e7d9a4e5ccc52fd9a93', 'state': 'manual', 'transient': False, 'is_filter_manual': True, 'is_mail_thread': True, 'is_mail_activity': True}
        model_vals['from_app_id'] = custom_module_id.id if custom_module_id else False
        model_id = env['ir.model'].create(model_vals)
        x_name = env['ir.model.fields'].search([('model_id', '=', model_id.id), ('name', '=', 'x_name')], limit=1)
        if x_name:
            x_name.unlink()
        
        #model access right

        access_vals = {'name': 'access_x_c68ffd06f8144e7d9a4e5ccc52fd9a93_user', 'perm_read': True, 'perm_write': True, 'perm_create': True, 'perm_unlink': True}
        group_id = env['res.groups'].search([('name', '=', 'Role / User')], limit=1)
        if not group_id:
            raise ValidationError('Group Role / User not found, please create it first.')

        access_vals['group_id'] = group_id.id
        access_vals['model_id'] = model_id.id
        env['ir.model.access'].create(access_vals)

        
        #model rules

        
        #model menus

        action_group_ids = []

        action_vals = {'name': 'Báo cáo kho ngày 2026-03-13 đến ngày 2026-03-14', 'name_id': 'Báo cáo tổng hợp', 'res_model': 'x_c68ffd06f8144e7d9a4e5ccc52fd9a93', 'type': 'ir.actions.act_window', 'usage': False, 'target': 'current', 'cache': True, 'view_mode': 'pivot', 'mobile_view_mode': 'kanban', 'domain': False, 'context': '{}', 'limit': 80, 'filter': False, 'help': Markup('<p class="o_view_nocontent_smiling_face">Create new document</p>')}
        action_vals['group_ids'] = [(6, 0, action_group_ids)]
        action_id = env['ir.actions.act_window'].create(action_vals)

        filter_user_ids = []

        filter_vals = {'name': 'Báo cáo kho ngày 2026-02-20 đến ngày 2026-02-22', 'model_id': 'x_c68ffd06f8144e7d9a4e5ccc52fd9a93', 'is_default': True, 'domain': '[("x_loai_ky", "!=", False)]', 'context': "{'group_by': [], 'pivot_measures': ['x_sl', 'x_tong_gia_tri'], 'pivot_column_groupby': ['x_loai_ky', 'x_kho_hang_id'], 'pivot_row_groupby': ['x_hang_hoa_id']}", 'sort': '[]'}
        filter_vals['action_id'] = action_id.id if action_id else False
        filter_vals['user_ids'] = [(6, 0, filter_user_ids)]
        env['ir.filters'].create(filter_vals)

        menu_group_ids = []

        group_137_ids = []

        menu_domain = [('name', '=', 'Quản lý kho'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Quản lý kho', 'sequence': 10, 'group_ids': [(6, 0, group_137_ids)], 'is_custom': True}
        if False:
            menu_domain.append(('parent_id', '=', False.id))
            menu_create_domain['parent_id'] = False.id
        menu_137 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_137:
            menu_137 = env['ir.ui.menu'].create(menu_create_domain)

        menu_vals = {'name': 'Báo cáo tổng hợp', 'sequence': 4, 'is_custom': True}
        menu_vals['action'] = f"ir.actions.act_window,{action_id.id}"
        menu_vals['group_ids'] = [(6, 0, menu_group_ids)]
        menu_vals['parent_id'] = menu_137.id if menu_137 else False
        env['ir.ui.menu'].create(menu_vals)

        action_group_ids = []

        action_vals = {'name': 'Sổ cái kho', 'name_id': False, 'res_model': 'x_c68ffd06f8144e7d9a4e5ccc52fd9a93', 'type': 'ir.actions.act_window', 'usage': False, 'target': 'current', 'cache': True, 'view_mode': 'list,form', 'mobile_view_mode': 'kanban', 'domain': False, 'context': '{}', 'limit': 80, 'filter': False, 'help': Markup('<p class="o_view_nocontent_smiling_face">Create new document</p>')}
        action_vals['group_ids'] = [(6, 0, action_group_ids)]
        action_id = env['ir.actions.act_window'].create(action_vals)

        filter_user_ids = []

        filter_vals = {'name': 'Sổ cái kho', 'model_id': 'x_c68ffd06f8144e7d9a4e5ccc52fd9a93', 'is_default': True, 'domain': '[]', 'context': "{'group_by': ['x_kho_hang_id', 'x_hang_hoa_id']}", 'sort': '[]'}
        filter_vals['action_id'] = action_id.id if action_id else False
        filter_vals['user_ids'] = [(6, 0, filter_user_ids)]
        env['ir.filters'].create(filter_vals)

        menu_group_ids = []

        group_137_ids = []

        menu_domain = [('name', '=', 'Quản lý kho'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Quản lý kho', 'sequence': 10, 'group_ids': [(6, 0, group_137_ids)], 'is_custom': True}
        if False:
            menu_domain.append(('parent_id', '=', False.id))
            menu_create_domain['parent_id'] = False.id
        menu_137 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_137:
            menu_137 = env['ir.ui.menu'].create(menu_create_domain)

        menu_vals = {'name': 'Sổ cái kho', 'sequence': 3, 'is_custom': True}
        menu_vals['action'] = f"ir.actions.act_window,{action_id.id}"
        menu_vals['group_ids'] = [(6, 0, menu_group_ids)]
        menu_vals['parent_id'] = menu_137.id if menu_137 else False
        env['ir.ui.menu'].create(menu_vals)

        
        #model views

        view_group_ids = []

        view_vals = {'name': 'Sổ cái kho pivot', 'model': 'x_c68ffd06f8144e7d9a4e5ccc52fd9a93', 'arch_base': '<pivot>\n    <field name="x_loai_ky" type="col"/>\n    <field name="x_kho_hang_id" type="col"/>\n    <field name="x_hang_hoa_id" type="row"/>\n    <field name="x_sl" type="measure"/>\n    <field name="x_tong_gia_tri" type="measure"/>\n    <field name="x_muc_dich"/>\n</pivot>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'pivot'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_c68ffd06f8144e7d9a4e5ccc52fd9a93.form', 'model': 'x_c68ffd06f8144e7d9a4e5ccc52fd9a93', 'arch_base': '<form>\n    <header/>\n    <sheet>\n        <group>\n            <field name="x_name"/>\n            <field name="x_ngay_thang"/>\n            <field name="x_sl"/>\n            <field name="x_gia_von"/>\n            <field name="x_tong_gia_tri"/>\n            <field name="x_muc_dich"/>\n            <field name="x_loai_chung_tu_id"/>\n            <field name="x_hang_hoa_id"/>\n            <field name="x_kho_hang_id"/>\n            <field name="x_cong_ty_id"/>\n            <field name="x_loai_ky"/>\n            <field name="x_ghi_chu"/>\n        </group>\n        <notebook/>\n    </sheet>\n    <chatter/>\n</form>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'form'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_c68ffd06f8144e7d9a4e5ccc52fd9a93.list', 'model': 'x_c68ffd06f8144e7d9a4e5ccc52fd9a93', 'arch_base': '<list editable="bottom">\n    <field name="x_name" optional="show"/>\n    <field name="x_ngay_thang" optional="show"/>\n    <field name="x_sl" optional="show"/>\n    <field name="x_gia_von" optional="show"/>\n    <field name="x_tong_gia_tri" optional="show"/>\n    <field name="x_muc_dich" optional="show"/>\n    <field name="x_loai_chung_tu_id" optional="show"/>\n    <field name="x_hang_hoa_id" optional="show"/>\n    <field name="x_kho_hang_id" optional="show"/>\n    <field name="x_cong_ty_id" optional="show"/>\n    <field name="x_loai_ky" optional="show"/>\n    <field name="x_ghi_chu" optional="show"/>\n</list>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'list'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_c68ffd06f8144e7d9a4e5ccc52fd9a93.search', 'model': 'x_c68ffd06f8144e7d9a4e5ccc52fd9a93', 'arch_base': '<search>\n    <field name="x_name"/>\n    <field name="x_ngay_thang"/>\n    <field name="x_sl"/>\n    <field name="x_gia_von"/>\n    <field name="x_tong_gia_tri"/>\n    <field name="x_muc_dich"/>\n    <field name="x_loai_chung_tu_id"/>\n    <field name="x_hang_hoa_id"/>\n    <field name="x_kho_hang_id"/>\n    <field name="x_cong_ty_id"/>\n    <field name="x_loai_ky"/>\n    <field name="x_ghi_chu"/>\n</search>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'search'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)


        #prepare fields for model Sổ cái kho

        groups = []
        field_vals = {'name': 'x_cong_ty_id', 'field_description': 'Công ty', 'ttype': 'many2one', 'help': False, 'sequence': 9, 'relation': 'x_1745d805e04a43b688d51b8267cc56fe', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_ghi_chu', 'field_description': 'Ghi chú', 'ttype': 'text', 'help': False, 'sequence': 11, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_gia_von', 'field_description': 'Định giá', 'ttype': 'float', 'help': False, 'sequence': 3, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_hang_hoa_id', 'field_description': 'Hàng hoá', 'ttype': 'many2one', 'help': False, 'sequence': 7, 'relation': 'x_9e57e8e385ca48d1b28e1cf1d646b8b6', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_kho_hang_id', 'field_description': 'Kho hàng', 'ttype': 'many2one', 'help': False, 'sequence': 8, 'relation': 'x_48c748e1bb1047d3ad931c4535cc12cf', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_loai_chung_tu_id', 'field_description': 'Loại chứng từ', 'ttype': 'reference', 'help': False, 'sequence': 6, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['selection_vals'].append({'sequence': 0, 'value': 'x_f0637b5ecea4413289b8fee8086af2e0', 'name': 'Xuất nhập kho'})

        field_vals['selection_vals'].append({'sequence': 1, 'value': 'x_77605823c2c743a19dfe7674cdbca3bd', 'name': 'Mua bán hàng hoá'})

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_loai_ky', 'field_description': 'Loại kỳ', 'ttype': 'selection', 'help': False, 'sequence': 10, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['selection_vals'].append({'sequence': 0, 'value': 'Tồn đầu kỳ', 'name': 'Tồn đầu kỳ'})

        field_vals['selection_vals'].append({'sequence': 1, 'value': 'Nhập trong kỳ', 'name': 'Nhập trong kỳ'})

        field_vals['selection_vals'].append({'sequence': 2, 'value': 'Xuất bán trong kỳ', 'name': 'Xuất bán trong kỳ'})

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_muc_dich', 'field_description': 'Mục đích', 'ttype': 'selection', 'help': False, 'sequence': 5, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['selection_vals'].append({'sequence': 0, 'value': 'Nhập hàng', 'name': 'Nhập hàng'})

        field_vals['selection_vals'].append({'sequence': 1, 'value': 'Xuất hàng', 'name': 'Xuất hàng'})

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_name', 'field_description': 'Name', 'ttype': 'char', 'help': False, 'sequence': 0, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': True, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_ngay_thang', 'field_description': 'Ngày tháng', 'ttype': 'datetime', 'help': False, 'sequence': 1, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_sl', 'field_description': 'Số lượng', 'ttype': 'float', 'help': False, 'sequence': 2, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_tong_gia_tri', 'field_description': 'Tổng giá trị', 'ttype': 'float', 'help': False, 'sequence': 4, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': True, 'invisible': False, 'store': True, 'index': False, 'copied': False, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        #model Sổ cái kế toán
        model_vals = {'name': 'Sổ cái kế toán', 'model': 'x_07c472ed342844baa780906b13dba020', 'state': 'manual', 'transient': False, 'is_filter_manual': True, 'is_mail_thread': True, 'is_mail_activity': True}
        model_vals['from_app_id'] = custom_module_id.id if custom_module_id else False
        model_id = env['ir.model'].create(model_vals)
        x_name = env['ir.model.fields'].search([('model_id', '=', model_id.id), ('name', '=', 'x_name')], limit=1)
        if x_name:
            x_name.unlink()
        
        #model access right

        access_vals = {'name': 'access_x_07c472ed342844baa780906b13dba020_user', 'perm_read': True, 'perm_write': True, 'perm_create': True, 'perm_unlink': True}
        group_id = env['res.groups'].search([('name', '=', 'Role / User')], limit=1)
        if not group_id:
            raise ValidationError('Group Role / User not found, please create it first.')

        access_vals['group_id'] = group_id.id
        access_vals['model_id'] = model_id.id
        env['ir.model.access'].create(access_vals)

        
        #model rules

        
        #model menus

        action_group_ids = []

        action_vals = {'name': 'Sổ cái kế toán', 'name_id': False, 'res_model': 'x_07c472ed342844baa780906b13dba020', 'type': 'ir.actions.act_window', 'usage': False, 'target': 'current', 'cache': True, 'view_mode': 'list,form', 'mobile_view_mode': 'kanban', 'domain': False, 'context': '{}', 'limit': 80, 'filter': False, 'help': Markup('<p class="o_view_nocontent_smiling_face">Create new document</p>')}
        action_vals['group_ids'] = [(6, 0, action_group_ids)]
        action_id = env['ir.actions.act_window'].create(action_vals)

        filter_user_ids = []

        filter_vals = {'name': 'Profit and loss', 'model_id': 'x_07c472ed342844baa780906b13dba020', 'is_default': False, 'domain': '[("x_report_type", "=", "Profit and Loss")]', 'context': "{'group_by': ['x_report_type', 'x_tai_khoan_id']}", 'sort': '[]'}
        filter_vals['action_id'] = action_id.id if action_id else False
        filter_vals['user_ids'] = [(6, 0, filter_user_ids)]
        env['ir.filters'].create(filter_vals)

        filter_user_ids = []

        filter_vals = {'name': 'Sổ cái kế toán', 'model_id': 'x_07c472ed342844baa780906b13dba020', 'is_default': True, 'domain': '[]', 'context': "{'group_by': ['x_report_type', 'x_root_type', 'x_tai_khoan_id']}", 'sort': '[]'}
        filter_vals['action_id'] = action_id.id if action_id else False
        filter_vals['user_ids'] = [(6, 0, filter_user_ids)]
        env['ir.filters'].create(filter_vals)

        filter_user_ids = []

        filter_vals = {'name': 'tài khoản', 'model_id': 'x_07c472ed342844baa780906b13dba020', 'is_default': False, 'domain': '[]', 'context': "{'group_by': ['x_tai_khoan_id']}", 'sort': '[]'}
        filter_vals['action_id'] = action_id.id if action_id else False
        filter_vals['user_ids'] = [(6, 0, filter_user_ids)]
        env['ir.filters'].create(filter_vals)

        menu_group_ids = []

        group_128_ids = []

        menu_domain = [('name', '=', 'Kế toán'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Kế toán', 'sequence': 11, 'group_ids': [(6, 0, group_128_ids)], 'is_custom': True}
        if False:
            menu_domain.append(('parent_id', '=', False.id))
            menu_create_domain['parent_id'] = False.id
        menu_128 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_128:
            menu_128 = env['ir.ui.menu'].create(menu_create_domain)

        menu_vals = {'name': 'Sổ cái kế toán', 'sequence': 1, 'is_custom': True}
        menu_vals['action'] = f"ir.actions.act_window,{action_id.id}"
        menu_vals['group_ids'] = [(6, 0, menu_group_ids)]
        menu_vals['parent_id'] = menu_128.id if menu_128 else False
        env['ir.ui.menu'].create(menu_vals)

        
        #model views

        view_group_ids = []

        view_vals = {'name': 'x_07c472ed342844baa780906b13dba020.form', 'model': 'x_07c472ed342844baa780906b13dba020', 'arch_base': '<form>\n    <header/>\n    <sheet>\n        <group>\n            <field name="x_name"/>\n            <field name="x_ngay_thang"/>\n            <field name="x_tai_khoan_id"/>\n            <field name="x_debit"/>\n            <field name="x_credit"/>\n            <field name="x_balance"/>\n            <field name="x_loai_chung_tu_id"/>\n            <field name="x_tk_doi_ung"/>\n            <field name="x_dai_ly_id"/>\n            <field name="x_cong_ty_id"/>\n            <field name="x_parent_id"/>\n            <field name="x_root_type"/>\n            <field name="x_report_type"/>\n            <field name="x_account_type"/>\n            <field name="x_ghi_chu"/>\n            <field name="x_bt_dc_id"/>\n        </group>\n        <notebook/>\n    </sheet>\n    <chatter/>\n</form>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'form'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_07c472ed342844baa780906b13dba020.list', 'model': 'x_07c472ed342844baa780906b13dba020', 'arch_base': '<list editable="bottom">\n    <field name="x_name" optional="show"/>\n    <field name="x_ngay_thang" optional="show"/>\n    <field name="x_tai_khoan_id" optional="show"/>\n    <field name="x_debit" optional="show"/>\n    <field name="x_credit" optional="show"/>\n    <field name="x_balance" optional="show" sum="Lợi nhuận"/>\n    <field name="x_loai_chung_tu_id" optional="show"/>\n    <field name="x_tk_doi_ung" optional="show"/>\n    <field name="x_dai_ly_id" optional="show"/>\n    <field name="x_cong_ty_id" optional="show"/>\n    <field name="x_parent_id" optional="show"/>\n    <field name="x_root_type" optional="show"/>\n    <field name="x_report_type" optional="show"/>\n    <field name="x_account_type" optional="show"/>\n    <field name="x_ghi_chu" optional="show"/>\n    <field name="x_bt_dc_id" optional="show"/>\n</list>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'list'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_07c472ed342844baa780906b13dba020.search', 'model': 'x_07c472ed342844baa780906b13dba020', 'arch_base': '<search>\n    <field name="x_name"/>\n    <field name="x_ngay_thang"/>\n    <field name="x_tai_khoan_id"/>\n    <field name="x_debit"/>\n    <field name="x_credit"/>\n    <field name="x_balance"/>\n    <field name="x_loai_chung_tu_id"/>\n    <field name="x_tk_doi_ung"/>\n    <field name="x_dai_ly_id"/>\n    <field name="x_cong_ty_id"/>\n    <field name="x_parent_id"/>\n    <field name="x_root_type"/>\n    <field name="x_report_type"/>\n    <field name="x_account_type"/>\n    <field name="x_ghi_chu"/>\n    <field name="x_bt_dc_id"/>\n</search>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'search'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)


        #prepare fields for model Sổ cái kế toán

        groups = []
        field_vals = {'name': 'x_account_type', 'field_description': 'Account Type', 'ttype': 'selection', 'help': False, 'sequence': 13, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': 'x_tai_khoan_id.x_account_type', 'depends': False, 'compute': False, 'required': False, 'readonly': True, 'invisible': False, 'store': True, 'index': False, 'copied': False, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_balance', 'field_description': 'Balance', 'ttype': 'float', 'help': False, 'sequence': 5, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': False, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_bt_dc_id', 'field_description': 'Bút toán điều chỉnh', 'ttype': 'many2one', 'help': False, 'sequence': 15, 'relation': 'x_c81b7d76356048f2beaf302b92b63806', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'cascade', 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_cong_ty_id', 'field_description': 'Công ty', 'ttype': 'many2one', 'help': False, 'sequence': 9, 'relation': 'x_1745d805e04a43b688d51b8267cc56fe', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_credit', 'field_description': 'Có', 'ttype': 'float', 'help': False, 'sequence': 4, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_dai_ly_id', 'field_description': 'Đại lý', 'ttype': 'many2one', 'help': False, 'sequence': 8, 'relation': 'x_47586e8c7d9744c3a1f1992a10a30b16', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_debit', 'field_description': 'Nợ', 'ttype': 'float', 'help': False, 'sequence': 3, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_ghi_chu', 'field_description': 'Ghi chú', 'ttype': 'text', 'help': False, 'sequence': 14, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_loai_chung_tu_id', 'field_description': 'Loại chứng từ', 'ttype': 'reference', 'help': False, 'sequence': 6, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['selection_vals'].append({'sequence': 0, 'value': 'x_7076d1049e954d7985d7e2cd445e5b20', 'name': 'Nhật ký thanh toán'})

        field_vals['selection_vals'].append({'sequence': 1, 'value': 'x_c90f6c65498d4983bdf0d7371f40618b', 'name': 'Phiếu kho'})

        field_vals['selection_vals'].append({'sequence': 2, 'value': 'x_3719e3f84afb4332a727a7a10419d8f7', 'name': 'HĐ mua bán'})

        field_vals['selection_vals'].append({'sequence': 3, 'value': 'x_c81b7d76356048f2beaf302b92b63806', 'name': 'Bút toán điều chỉnh'})

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_name', 'field_description': 'Name', 'ttype': 'char', 'help': False, 'sequence': 0, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': True, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_ngay_thang', 'field_description': 'Ngày tháng', 'ttype': 'datetime', 'help': False, 'sequence': 1, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_parent_id', 'field_description': 'Parent Account', 'ttype': 'many2one', 'help': False, 'sequence': 10, 'relation': 'x_500b7a5ea68541cb82fc5cc4e7be7c6a', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': 'x_tai_khoan_id.x_parent_id', 'depends': False, 'compute': False, 'required': False, 'readonly': True, 'invisible': False, 'store': True, 'index': False, 'copied': False, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_report_type', 'field_description': 'Report Type', 'ttype': 'selection', 'help': False, 'sequence': 12, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': 'x_tai_khoan_id.x_report_type', 'depends': False, 'compute': False, 'required': False, 'readonly': True, 'invisible': False, 'store': True, 'index': False, 'copied': False, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_root_type', 'field_description': 'Root Type', 'ttype': 'selection', 'help': False, 'sequence': 11, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': 'x_tai_khoan_id.x_root_type', 'depends': False, 'compute': False, 'required': False, 'readonly': True, 'invisible': False, 'store': True, 'index': False, 'copied': False, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_tai_khoan_id', 'field_description': 'Tài khoản', 'ttype': 'many2one', 'help': False, 'sequence': 2, 'relation': 'x_500b7a5ea68541cb82fc5cc4e7be7c6a', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_tk_doi_ung', 'field_description': 'Tài khoản đối ứng', 'ttype': 'char', 'help': False, 'sequence': 7, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        #model Tài khoản
        model_vals = {'name': 'Tài khoản', 'model': 'x_500b7a5ea68541cb82fc5cc4e7be7c6a', 'state': 'manual', 'transient': False, 'is_filter_manual': True, 'is_mail_thread': True, 'is_mail_activity': True}
        model_vals['from_app_id'] = custom_module_id.id if custom_module_id else False
        model_id = env['ir.model'].create(model_vals)
        x_name = env['ir.model.fields'].search([('model_id', '=', model_id.id), ('name', '=', 'x_name')], limit=1)
        if x_name:
            x_name.unlink()
        
        #model access right

        access_vals = {'name': 'access_x_500b7a5ea68541cb82fc5cc4e7be7c6a_user', 'perm_read': True, 'perm_write': True, 'perm_create': True, 'perm_unlink': True}
        group_id = env['res.groups'].search([('name', '=', 'Role / User')], limit=1)
        if not group_id:
            raise ValidationError('Group Role / User not found, please create it first.')

        access_vals['group_id'] = group_id.id
        access_vals['model_id'] = model_id.id
        env['ir.model.access'].create(access_vals)

        
        #model rules

        
        #model menus

        filter_user_ids = []

        filter_vals = {'name': 'account', 'model_id': 'x_500b7a5ea68541cb82fc5cc4e7be7c6a', 'is_default': True, 'domain': '[("x_is_group", "=", False)]', 'context': "{'group_by': []}", 'sort': '[]'}
        filter_vals['user_ids'] = [(6, 0, filter_user_ids)]
        env['ir.filters'].create(filter_vals)

        action_group_ids = []

        action_vals = {'name': 'Tài khoản', 'name_id': False, 'res_model': 'x_500b7a5ea68541cb82fc5cc4e7be7c6a', 'type': 'ir.actions.act_window', 'usage': False, 'target': 'current', 'cache': True, 'view_mode': 'list,form', 'mobile_view_mode': 'kanban', 'domain': False, 'context': '{}', 'limit': 80, 'filter': False, 'help': Markup('<p class="o_view_nocontent_smiling_face">Create new document</p>')}
        action_vals['group_ids'] = [(6, 0, action_group_ids)]
        action_id = env['ir.actions.act_window'].create(action_vals)

        menu_group_ids = []

        group_128_ids = []

        menu_domain = [('name', '=', 'Kế toán'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Kế toán', 'sequence': 11, 'group_ids': [(6, 0, group_128_ids)], 'is_custom': True}
        if False:
            menu_domain.append(('parent_id', '=', False.id))
            menu_create_domain['parent_id'] = False.id
        menu_128 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_128:
            menu_128 = env['ir.ui.menu'].create(menu_create_domain)

        menu_vals = {'name': 'Tài khoản', 'sequence': 2, 'is_custom': True}
        menu_vals['action'] = f"ir.actions.act_window,{action_id.id}"
        menu_vals['group_ids'] = [(6, 0, menu_group_ids)]
        menu_vals['parent_id'] = menu_128.id if menu_128 else False
        env['ir.ui.menu'].create(menu_vals)

        
        #model views

        view_group_ids = []

        view_vals = {'name': 'x_500b7a5ea68541cb82fc5cc4e7be7c6a.form', 'model': 'x_500b7a5ea68541cb82fc5cc4e7be7c6a', 'arch_base': '<form>\n    <header/>\n    <sheet>\n        <group>\n            <group>\n                <field name="x_is_group"/>\n                <field name="x_name"/>\n                <field name="x_account_number"/>\n                <field name="x_company_id"/>\n                <field name="x_currency_id"/>\n                <field name="x_root_type"/>\n                <field name="x_report_type"/>\n            </group>\n            <group>\n                <field name="x_parent_id"/>\n                <field name="x_account_type"/>\n                <field name="x_balance_must_be"/>\n            </group>\n        </group>\n        <notebook/>\n    </sheet>\n    <chatter/>\n</form>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'form'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_500b7a5ea68541cb82fc5cc4e7be7c6a.list', 'model': 'x_500b7a5ea68541cb82fc5cc4e7be7c6a', 'arch_base': '<list>\n    <field name="x_name" optional="show"/>\n    <field name="x_is_group" optional="show"/>\n    <field name="x_parent_id" optional="show"/>\n    <field name="x_currency_id" optional="show"/>\n    <field name="x_account_number" optional="show"/>\n    <field name="x_root_type" optional="show"/>\n    <field name="x_report_type" optional="show"/>\n    <field name="x_account_type" optional="show"/>\n    <field name="x_balance_must_be" optional="show"/>\n    <field name="x_company_id" optional="show"/>\n</list>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'list'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_500b7a5ea68541cb82fc5cc4e7be7c6a.search', 'model': 'x_500b7a5ea68541cb82fc5cc4e7be7c6a', 'arch_base': '<search>\n    <field name="x_name"/>\n    <field name="x_is_group"/>\n    <field name="x_parent_id"/>\n    <field name="x_currency_id"/>\n    <field name="x_account_number"/>\n    <field name="x_root_type"/>\n    <field name="x_report_type"/>\n    <field name="x_account_type"/>\n    <field name="x_balance_must_be"/>\n    <field name="x_company_id"/>\n    <searchpanel>\n        <field name="x_company_id"/>\n        <field name="x_parent_id"/>\n    </searchpanel>\n</search>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'search'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)


        #prepare fields for model Tài khoản

        groups = []
        field_vals = {'name': 'x_account_number', 'field_description': 'Account Number', 'ttype': 'integer', 'help': False, 'sequence': 4, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_account_type', 'field_description': 'Account Type', 'ttype': 'selection', 'help': False, 'sequence': 7, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['selection_vals'].append({'sequence': 0, 'value': 'Stock', 'name': 'Stock'})

        field_vals['selection_vals'].append({'sequence': 1, 'value': 'Stock Received But Not Billed', 'name': 'Stock Received But Not Billed'})

        field_vals['selection_vals'].append({'sequence': 2, 'value': 'Cost of Goods Sold', 'name': 'Cost of Goods Sold'})

        field_vals['selection_vals'].append({'sequence': 3, 'value': 'Stock Adjustment', 'name': 'Stock Adjustment'})

        field_vals['selection_vals'].append({'sequence': 4, 'value': 'Payable', 'name': 'Payable'})

        field_vals['selection_vals'].append({'sequence': 5, 'value': 'Receivable', 'name': 'Receivable'})

        field_vals['selection_vals'].append({'sequence': 6, 'value': 'Cash', 'name': 'Cash'})

        field_vals['selection_vals'].append({'sequence': 7, 'value': 'Bank', 'name': 'Bank'})

        field_vals['selection_vals'].append({'sequence': 8, 'value': 'Equity', 'name': 'Equity'})

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_balance_must_be', 'field_description': 'Balance must be', 'ttype': 'selection', 'help': False, 'sequence': 8, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['selection_vals'].append({'sequence': 0, 'value': 'Debit', 'name': 'Debit'})

        field_vals['selection_vals'].append({'sequence': 1, 'value': 'Credit', 'name': 'Credit'})

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_company_id', 'field_description': 'Company', 'ttype': 'many2one', 'help': False, 'sequence': 9, 'relation': 'x_1745d805e04a43b688d51b8267cc56fe', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_currency_id', 'field_description': 'Currency', 'ttype': 'many2one', 'help': False, 'sequence': 3, 'relation': 'res.currency', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_is_group', 'field_description': 'Is Group', 'ttype': 'boolean', 'help': False, 'sequence': 1, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_name', 'field_description': 'Name', 'ttype': 'char', 'help': False, 'sequence': 0, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_parent_id', 'field_description': 'Parent Account', 'ttype': 'many2one', 'help': False, 'sequence': 2, 'relation': 'x_500b7a5ea68541cb82fc5cc4e7be7c6a', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_report_type', 'field_description': 'Report Type', 'ttype': 'selection', 'help': False, 'sequence': 6, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['selection_vals'].append({'sequence': 0, 'value': 'Balance Sheet', 'name': 'Balance Sheet'})

        field_vals['selection_vals'].append({'sequence': 1, 'value': 'Profit and Loss', 'name': 'Profit and Loss'})

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_root_type', 'field_description': 'Root Type', 'ttype': 'selection', 'help': False, 'sequence': 5, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['selection_vals'].append({'sequence': 0, 'value': 'Asset', 'name': 'Asset'})

        field_vals['selection_vals'].append({'sequence': 1, 'value': 'Liability', 'name': 'Liability'})

        field_vals['selection_vals'].append({'sequence': 2, 'value': 'Income', 'name': 'Income'})

        field_vals['selection_vals'].append({'sequence': 3, 'value': 'Expense', 'name': 'Expense'})

        field_vals['selection_vals'].append({'sequence': 4, 'value': 'Equity', 'name': 'Equity'})

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        #model Xuất nhập kho
        model_vals = {'name': 'Xuất nhập kho', 'model': 'x_f0637b5ecea4413289b8fee8086af2e0', 'state': 'manual', 'transient': False, 'is_filter_manual': True, 'is_mail_thread': True, 'is_mail_activity': True}
        model_vals['from_app_id'] = custom_module_id.id if custom_module_id else False
        model_id = env['ir.model'].create(model_vals)
        x_name = env['ir.model.fields'].search([('model_id', '=', model_id.id), ('name', '=', 'x_name')], limit=1)
        if x_name:
            x_name.unlink()
        
        #model access right

        access_vals = {'name': 'access_x_f0637b5ecea4413289b8fee8086af2e0_user', 'perm_read': True, 'perm_write': True, 'perm_create': True, 'perm_unlink': True}
        group_id = env['res.groups'].search([('name', '=', 'Role / User')], limit=1)
        if not group_id:
            raise ValidationError('Group Role / User not found, please create it first.')

        access_vals['group_id'] = group_id.id
        access_vals['model_id'] = model_id.id
        env['ir.model.access'].create(access_vals)

        
        #model rules

        
        #model menus

        action_group_ids = []

        action_vals = {'name': 'Xuất nhập kho', 'name_id': False, 'res_model': 'x_f0637b5ecea4413289b8fee8086af2e0', 'type': 'ir.actions.act_window', 'usage': False, 'target': 'current', 'cache': True, 'view_mode': 'list,form', 'mobile_view_mode': 'kanban', 'domain': False, 'context': '{}', 'limit': 80, 'filter': False, 'help': Markup('<p class="o_view_nocontent_smiling_face">Create new document</p>')}
        action_vals['group_ids'] = [(6, 0, action_group_ids)]
        action_id = env['ir.actions.act_window'].create(action_vals)

        menu_group_ids = []

        group_137_ids = []

        menu_domain = [('name', '=', 'Quản lý kho'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Quản lý kho', 'sequence': 10, 'group_ids': [(6, 0, group_137_ids)], 'is_custom': True}
        if False:
            menu_domain.append(('parent_id', '=', False.id))
            menu_create_domain['parent_id'] = False.id
        menu_137 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_137:
            menu_137 = env['ir.ui.menu'].create(menu_create_domain)

        menu_vals = {'name': 'Xuất nhập kho', 'sequence': 2, 'is_custom': True}
        menu_vals['action'] = f"ir.actions.act_window,{action_id.id}"
        menu_vals['group_ids'] = [(6, 0, menu_group_ids)]
        menu_vals['parent_id'] = menu_137.id if menu_137 else False
        env['ir.ui.menu'].create(menu_vals)

        
        #model views

        view_group_ids = []

        view_vals = {'name': 'x_f0637b5ecea4413289b8fee8086af2e0.form', 'model': 'x_f0637b5ecea4413289b8fee8086af2e0', 'arch_base': '<form>\n    <header/>\n    <sheet>\n        <group>\n            <field name="x_name"/>\n            <field name="x_ngay_thang"/>\n            <field name="x_phieu_kho_id"/>\n            <field name="x_muc_dich"/>\n            <field name="x_kho_nguon_id"/>\n            <field name="x_kho_dich_id"/>\n            <field name="x_hang_hoa_id"/>\n            <field name="x_sl"/>\n            <field name="x_gia_von" readonly="x_muc_dich == \'Xuất hàng\'"/>\n            <field name="x_cong_ty_id"/>\n        </group>\n        <notebook/>\n    </sheet>\n    <chatter/>\n</form>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'form'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_f0637b5ecea4413289b8fee8086af2e0.list', 'model': 'x_f0637b5ecea4413289b8fee8086af2e0', 'arch_base': '<list editable="bottom" open_form_view="true">\n    <field name="x_name" optional="show"/>\n    <field name="x_ngay_thang" optional="show"/>\n    <field name="x_phieu_kho_id" optional="show" context="{\'is_hide\': not x_phieu_kho_id}"/>\n    <field name="x_muc_dich" optional="show"/>\n    <field name="x_kho_nguon_id" optional="show"/>\n    <field name="x_kho_dich_id" optional="show"/>\n    <field name="x_hang_hoa_id" optional="show"/>\n    <field name="x_sl" optional="show"/>\n    <field name="x_gia_von" optional="show" readonly="x_muc_dich == \'Xuất hàng\'"/>\n    <field name="x_cong_ty_id" optional="show"/>\n</list>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'list'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_f0637b5ecea4413289b8fee8086af2e0.search', 'model': 'x_f0637b5ecea4413289b8fee8086af2e0', 'arch_base': '<search>\n    <field name="x_name"/>\n    <field name="x_ngay_thang"/>\n    <field name="x_phieu_kho_id"/>\n    <field name="x_muc_dich"/>\n    <field name="x_kho_nguon_id"/>\n    <field name="x_kho_dich_id"/>\n    <field name="x_hang_hoa_id"/>\n    <field name="x_sl"/>\n    <field name="x_gia_von"/>\n    <field name="x_cong_ty_id"/>\n</search>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'search'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)


        #prepare fields for model Xuất nhập kho

        groups = []
        field_vals = {'name': 'x_cong_ty_id', 'field_description': 'Công ty', 'ttype': 'many2one', 'help': False, 'sequence': 9, 'relation': 'x_1745d805e04a43b688d51b8267cc56fe', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': 'x_phieu_kho_id.x_cong_ty_id', 'depends': False, 'compute': False, 'required': False, 'readonly': True, 'invisible': False, 'store': True, 'index': False, 'copied': False, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_gia_von', 'field_description': 'Giá trị', 'ttype': 'float', 'help': False, 'sequence': 8, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_hang_hoa_id', 'field_description': 'Tên hàng hoá', 'ttype': 'many2one', 'help': False, 'sequence': 6, 'relation': 'x_9e57e8e385ca48d1b28e1cf1d646b8b6', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_kho_dich_id', 'field_description': 'Kho đích', 'ttype': 'many2one', 'help': False, 'sequence': 5, 'relation': 'x_48c748e1bb1047d3ad931c4535cc12cf', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': True, 'invisible': False, 'store': True, 'index': False, 'copied': False, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_kho_nguon_id', 'field_description': 'Kho nguồn', 'ttype': 'many2one', 'help': False, 'sequence': 4, 'relation': 'x_48c748e1bb1047d3ad931c4535cc12cf', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': True, 'invisible': False, 'store': True, 'index': False, 'copied': False, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_mo_ta', 'field_description': 'Mô tả', 'ttype': 'char', 'help': False, 'sequence': 10, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_muc_dich', 'field_description': 'Mục đích', 'ttype': 'selection', 'help': False, 'sequence': 3, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['selection_vals'].append({'sequence': 0, 'value': 'Nhập hàng', 'name': 'Nhập hàng'})

        field_vals['selection_vals'].append({'sequence': 1, 'value': 'Xuất hàng', 'name': 'Xuất hàng'})

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_name', 'field_description': 'Name', 'ttype': 'char', 'help': False, 'sequence': 0, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': True, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_ngay_thang', 'field_description': 'Ngày tháng', 'ttype': 'datetime', 'help': False, 'sequence': 1, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': 'x_phieu_kho_id.x_ngay_thang', 'depends': False, 'compute': False, 'required': False, 'readonly': True, 'invisible': False, 'store': True, 'index': False, 'copied': False, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_phieu_kho_id', 'field_description': 'Phiếu kho', 'ttype': 'many2one', 'help': False, 'sequence': 2, 'relation': 'x_c90f6c65498d4983bdf0d7371f40618b', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_sl', 'field_description': 'Số lượng', 'ttype': 'float', 'help': False, 'sequence': 7, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        #model Đại lý
        model_vals = {'name': 'Đại lý', 'model': 'x_47586e8c7d9744c3a1f1992a10a30b16', 'state': 'manual', 'transient': False, 'is_filter_manual': True, 'is_mail_thread': True, 'is_mail_activity': True}
        model_vals['from_app_id'] = custom_module_id.id if custom_module_id else False
        model_id = env['ir.model'].create(model_vals)
        x_name = env['ir.model.fields'].search([('model_id', '=', model_id.id), ('name', '=', 'x_name')], limit=1)
        if x_name:
            x_name.unlink()
        
        #model access right

        access_vals = {'name': 'access_x_47586e8c7d9744c3a1f1992a10a30b16_user', 'perm_read': True, 'perm_write': True, 'perm_create': True, 'perm_unlink': True}
        group_id = env['res.groups'].search([('name', '=', 'Role / User')], limit=1)
        if not group_id:
            raise ValidationError('Group Role / User not found, please create it first.')

        access_vals['group_id'] = group_id.id
        access_vals['model_id'] = model_id.id
        env['ir.model.access'].create(access_vals)

        
        #model rules

        
        #model menus

        action_group_ids = []

        action_vals = {'name': 'Đại lý', 'name_id': False, 'res_model': 'x_47586e8c7d9744c3a1f1992a10a30b16', 'type': 'ir.actions.act_window', 'usage': False, 'target': 'current', 'cache': True, 'view_mode': 'list,form', 'mobile_view_mode': 'kanban', 'domain': False, 'context': '{}', 'limit': 80, 'filter': False, 'help': Markup('<p class="o_view_nocontent_smiling_face">Create new document</p>')}
        action_vals['group_ids'] = [(6, 0, action_group_ids)]
        action_id = env['ir.actions.act_window'].create(action_vals)

        menu_group_ids = []

        group_131_ids = []

        menu_domain = [('name', '=', 'Bán hàng'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Bán hàng', 'sequence': 9, 'group_ids': [(6, 0, group_131_ids)], 'is_custom': True}
        if False:
            menu_domain.append(('parent_id', '=', False.id))
            menu_create_domain['parent_id'] = False.id
        menu_131 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_131:
            menu_131 = env['ir.ui.menu'].create(menu_create_domain)

        menu_vals = {'name': 'Đại lý', 'sequence': 1, 'is_custom': True}
        menu_vals['action'] = f"ir.actions.act_window,{action_id.id}"
        menu_vals['group_ids'] = [(6, 0, menu_group_ids)]
        menu_vals['parent_id'] = menu_131.id if menu_131 else False
        env['ir.ui.menu'].create(menu_vals)

        
        #model views

        view_group_ids = []

        view_vals = {'name': 'x_47586e8c7d9744c3a1f1992a10a30b16.form', 'model': 'x_47586e8c7d9744c3a1f1992a10a30b16', 'arch_base': '<form>\n    <header/>\n    <sheet>\n        <group>\n            <field name="x_name"/>\n            <field name="x_dsg_id"/>\n        </group>\n        <notebook/>\n    </sheet>\n    <chatter/>\n</form>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'form'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_47586e8c7d9744c3a1f1992a10a30b16.list', 'model': 'x_47586e8c7d9744c3a1f1992a10a30b16', 'arch_base': '<list>\n    <field name="x_name" optional="show"/>\n    <field name="x_dsg_id" optional="show"/>\n</list>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'list'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_47586e8c7d9744c3a1f1992a10a30b16.search', 'model': 'x_47586e8c7d9744c3a1f1992a10a30b16', 'arch_base': '<search>\n    <field name="x_name"/>\n    <field name="x_dsg_id"/>\n</search>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'search'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)


        #prepare fields for model Đại lý

        groups = []
        field_vals = {'name': 'x_dsg_id', 'field_description': 'Danh sách giá', 'ttype': 'many2one', 'help': False, 'sequence': 1, 'relation': 'x_7007229d76ad42cd853707f65fd26e33', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_name', 'field_description': 'Name', 'ttype': 'char', 'help': False, 'sequence': 0, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        #model model Sổ cái
        model_vals = {'name': 'model Sổ cái', 'model': 'x_model_so_cai', 'state': 'manual', 'transient': True, 'is_filter_manual': True, 'is_mail_thread': False, 'is_mail_activity': False}
        model_vals['from_app_id'] = custom_module_id.id if custom_module_id else False
        model_id = env['ir.model'].create(model_vals)
        x_name = env['ir.model.fields'].search([('model_id', '=', model_id.id), ('name', '=', 'x_name')], limit=1)
        if x_name:
            x_name.unlink()
        
        #model access right

        access_vals = {'name': 'ok', 'perm_read': True, 'perm_write': True, 'perm_create': True, 'perm_unlink': True}
        group_id = env['res.groups'].search([('name', '=', 'Role / User')], limit=1)
        if not group_id:
            raise ValidationError('Group Role / User not found, please create it first.')

        access_vals['group_id'] = group_id.id
        access_vals['model_id'] = model_id.id
        env['ir.model.access'].create(access_vals)

        
        #model rules

        
        #model menus

        action_group_ids = []

        action_vals = {'name': 'Model sổ cái', 'name_id': 'Model sổ cái', 'res_model': 'x_model_so_cai', 'type': 'ir.actions.act_window', 'usage': False, 'target': 'new', 'cache': True, 'view_mode': 'form', 'mobile_view_mode': 'kanban', 'domain': False, 'context': '{}', 'limit': 80, 'filter': False, 'help': False}
        action_vals['group_ids'] = [(6, 0, action_group_ids)]
        action_id = env['ir.actions.act_window'].create(action_vals)

        menu_group_ids = []

        group_id = env['res.groups'].search([('uuid', '=', 'uuid_Role_Administrator')], limit=1)

        if not group_id:
            group_vals = {'name': 'Role / Administrator', 'uuid': 'uuid_Role_Administrator', 'share': False, 'sequence': 0, 'api_key_duration': 0.0, 'comment': 'Access to the settings to configure the apps'}
            privilege_id = env['res.groups.privilege'].search([('uuid', '=', 'False')], limit=1)
            if False and not privilege_id:
                privilege_vals = {}
                privilege_id = env['res.groups.privilege'].create(privilege_vals)
            group_vals['privilege_id'] = privilege_id.id if privilege_id else False
            group_id = env['res.groups'].create(group_vals)

        menu_group_ids.append(group_id.id)

        group_137_ids = []

        menu_domain = [('name', '=', 'Quản lý kho'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Quản lý kho', 'sequence': 10, 'group_ids': [(6, 0, group_137_ids)], 'is_custom': True}
        if False:
            menu_domain.append(('parent_id', '=', False.id))
            menu_create_domain['parent_id'] = False.id
        menu_137 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_137:
            menu_137 = env['ir.ui.menu'].create(menu_create_domain)

        menu_vals = {'name': 'Model sổ cái', 'sequence': 10, 'is_custom': True}
        menu_vals['action'] = f"ir.actions.act_window,{action_id.id}"
        menu_vals['group_ids'] = [(6, 0, menu_group_ids)]
        menu_vals['parent_id'] = menu_137.id if menu_137 else False
        env['ir.ui.menu'].create(menu_vals)

        
        #model views

        view_group_ids = []

        view_vals = {'name': 'form', 'model': 'x_model_so_cai', 'arch_base': '<form>\n    <header/>\n    <sheet>\n        <group>\n            <!--<field name="x_name"/>-->\n            <field name="x_tu_ngay"/>\n            <field name="x_den_ngay"/>\n        </group>\n        <notebook/>\n        <footer>\n            <button name="1" string="OK" type="action" class="btn-primary"/>\n            <button string="Cancel" class="btn-secondary" special="cancel"/>\n        </footer>\n    </sheet>\n    <chatter/>\n</form>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'form'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)


        #prepare fields for model model Sổ cái

        groups = []
        field_vals = {'name': 'x_den_ngay', 'field_description': 'Đến ngày', 'ttype': 'date', 'help': False, 'sequence': 2, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_name', 'field_description': 'Name', 'ttype': 'char', 'help': False, 'sequence': 0, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_tu_ngay', 'field_description': 'Từ ngày', 'ttype': 'date', 'help': False, 'sequence': 1, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        #model model thanh toan
        model_vals = {'name': 'model thanh toan', 'model': 'x_model_thanh_toan', 'state': 'manual', 'transient': True, 'is_filter_manual': True, 'is_mail_thread': False, 'is_mail_activity': False}
        model_vals['from_app_id'] = custom_module_id.id if custom_module_id else False
        model_id = env['ir.model'].create(model_vals)
        x_name = env['ir.model.fields'].search([('model_id', '=', model_id.id), ('name', '=', 'x_name')], limit=1)
        if x_name:
            x_name.unlink()
        
        #model access right

        access_vals = {'name': 'allow', 'perm_read': True, 'perm_write': True, 'perm_create': True, 'perm_unlink': True}
        group_id = env['res.groups'].search([('name', '=', 'Role / User')], limit=1)
        if not group_id:
            raise ValidationError('Group Role / User not found, please create it first.')

        access_vals['group_id'] = group_id.id
        access_vals['model_id'] = model_id.id
        env['ir.model.access'].create(access_vals)

        
        #model rules

        
        #model menus

        action_group_ids = []

        action_vals = {'name': 'Thanh toán', 'name_id': False, 'res_model': 'x_model_thanh_toan', 'type': 'ir.actions.act_window', 'usage': False, 'target': 'new', 'cache': True, 'view_mode': 'form', 'mobile_view_mode': 'kanban', 'domain': False, 'context': "{'x_hd_id': False}", 'limit': 80, 'filter': False, 'help': False}
        action_vals['group_ids'] = [(6, 0, action_group_ids)]
        action_id = env['ir.actions.act_window'].create(action_vals)

        menu_group_ids = []

        group_id = env['res.groups'].search([('uuid', '=', 'uuid_Role_Administrator')], limit=1)

        if not group_id:
            group_vals = {'name': 'Role / Administrator', 'uuid': 'uuid_Role_Administrator', 'share': False, 'sequence': 0, 'api_key_duration': 0.0, 'comment': 'Access to the settings to configure the apps'}
            privilege_id = env['res.groups.privilege'].search([('uuid', '=', 'False')], limit=1)
            if False and not privilege_id:
                privilege_vals = {}
                privilege_id = env['res.groups.privilege'].create(privilege_vals)
            group_vals['privilege_id'] = privilege_id.id if privilege_id else False
            group_id = env['res.groups'].create(group_vals)

        menu_group_ids.append(group_id.id)

        group_131_ids = []

        menu_domain = [('name', '=', 'Bán hàng'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Bán hàng', 'sequence': 9, 'group_ids': [(6, 0, group_131_ids)], 'is_custom': True}
        if False:
            menu_domain.append(('parent_id', '=', False.id))
            menu_create_domain['parent_id'] = False.id
        menu_131 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_131:
            menu_131 = env['ir.ui.menu'].create(menu_create_domain)

        menu_vals = {'name': 'Thanh toán', 'sequence': 10, 'is_custom': True}
        menu_vals['action'] = f"ir.actions.act_window,{action_id.id}"
        menu_vals['group_ids'] = [(6, 0, menu_group_ids)]
        menu_vals['parent_id'] = menu_131.id if menu_131 else False
        env['ir.ui.menu'].create(menu_vals)

        
        #model views

        view_group_ids = []

        view_vals = {'name': 'form', 'model': 'x_model_thanh_toan', 'arch_base': '<form>\n    <header/>\n    <sheet>\n        <group>\n            <field name="x_name" invisible="1"/>\n            <field name="x_ngay_thang"/>\n            <field name="x_thanh_toan"/>\n            <field name="x_loai_thanh_toan"/>\n            <field name="x_chuc_nang"/>\n        </group>\n        <notebook/>\n        <footer>\n            <button name="1" type="action" string="Xác nhận" class="btn-primary"/>\n            <button special="cancel" string="Huỷ" class="btn-secondary"/>\n        </footer>\n    </sheet>\n    <chatter/>\n</form>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'form'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)


        #prepare fields for model model thanh toan

        groups = []
        field_vals = {'name': 'x_chuc_nang', 'field_description': 'Chức năng', 'ttype': 'selection', 'help': False, 'sequence': 5, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['selection_vals'].append({'sequence': 0, 'value': 'Xoá cũ tạo mới', 'name': 'Xoá cũ tạo mới'})

        field_vals['selection_vals'].append({'sequence': 1, 'value': 'Thêm tiền', 'name': 'Thêm tiền'})

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_loai_thanh_toan', 'field_description': 'Loại thanh toán', 'ttype': 'selection', 'help': False, 'sequence': 4, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['selection_vals'].append({'sequence': 0, 'value': 'Tiền mặt', 'name': 'Tiền mặt'})

        field_vals['selection_vals'].append({'sequence': 1, 'value': 'Ngân hàng', 'name': 'Ngân hàng'})

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_name', 'field_description': 'Name', 'ttype': 'char', 'help': False, 'sequence': 0, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': True, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_ngay_thang', 'field_description': 'Ngày tháng', 'ttype': 'datetime', 'help': False, 'sequence': 2, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_thanh_toan', 'field_description': 'Số tiền', 'ttype': 'float', 'help': False, 'sequence': 3, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
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
        if related or related or related:
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

    model_id = env['ir.model'].search([('model', '=', 'x_c81b7d76356048f2beaf302b92b63806')])

    trigger_field_ids = []
    on_change_field_ids = []

    auto_vals = {'name': 'ref', 'trigger': 'on_create', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    sequence_id = env['ir.sequence'].create({'name': 'Bút toán điều chỉnh', 'implementation': 'standard', 'code': 'x_c81b7d76356048f2beaf302b92b63806', 'active': True, 'prefix': 'BTDC-', 'suffix': False, 'padding': 4, 'number_increment': 1, 'use_date_range': False})

    action_vals = {'name': 'Update Bút toán điều chỉnh', 'sequence': 5, 'state': 'object_write', 'code': False, 'evaluation_type': 'sequence', 'update_path': 'x_name', 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'x_name'), ('model', '=', 'x_c81b7d76356048f2beaf302b92b63806')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    trigger_field_ids = []
    on_change_field_ids = []

    field_id = env['ir.model.fields'].search([('model_id', '=', 'x_c81b7d76356048f2beaf302b92b63806'), ('name', '=', 'x_name')])
    on_change_field_ids.append(field_id.id)

    auto_vals = {'name': 'default', 'trigger': 'on_change', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    action_vals = {'name': 'Execute Code', 'sequence': 5, 'state': 'code', 'code': 'DISPLAY_SEQUENCE()\nrecord.write({"x_ngay_thang": datetime.datetime.now()})\n', 'evaluation_type': 'value', 'update_path': False, 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'False'), ('model', '=', 'False')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    trigger_field_ids = []
    on_change_field_ids = []

    field_id = env['ir.model.fields'].search([('model_id', '=', 'x_c81b7d76356048f2beaf302b92b63806'), ('name', '=', 'x_cong_ty_id')])
    on_change_field_ids.append(field_id.id)

    field_id = env['ir.model.fields'].search([('model_id', '=', 'x_c81b7d76356048f2beaf302b92b63806'), ('name', '=', 'x_ngay_thang')])
    on_change_field_ids.append(field_id.id)

    auto_vals = {'name': 'set items x_ngay_thang', 'trigger': 'on_change', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    action_vals = {'name': 'Execute Code', 'sequence': 5, 'state': 'code', 'code': 'record.x_items.write({\n    "x_ngay_thang": record.x_ngay_thang,\n    "x_cong_ty_id": record.x_cong_ty_id.id,\n    "x_ghi_chu": record.x_ghi_chu\n})\n', 'evaluation_type': 'value', 'update_path': False, 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'False'), ('model', '=', 'False')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    trigger_field_ids = []
    on_change_field_ids = []

    auto_vals = {'name': 'set items x_ngay_thang after edit', 'trigger': 'on_create_or_write', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    action_vals = {'name': 'Execute Code', 'sequence': 5, 'state': 'code', 'code': 'record.x_items.write({\n    "x_ngay_thang": record.x_ngay_thang,\n    "x_cong_ty_id": record.x_cong_ty_id.id,\n    "x_ghi_chu": record.x_ghi_chu\n})\n', 'evaluation_type': 'value', 'update_path': False, 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'False'), ('model', '=', 'False')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    model_id = env['ir.model'].search([('model', '=', 'x_1745d805e04a43b688d51b8267cc56fe')])

    model_id = env['ir.model'].search([('model', '=', 'x_7007229d76ad42cd853707f65fd26e33')])

    model_id = env['ir.model'].search([('model', '=', 'x_291da0ecd8dc4491b65b085a6adbb09a')])

    trigger_field_ids = []
    on_change_field_ids = []

    auto_vals = {'name': 'ref', 'trigger': 'on_create', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    sequence_id = env['ir.sequence'].create({'name': 'Giá hàng hoá', 'implementation': 'standard', 'code': 'x_291da0ecd8dc4491b65b085a6adbb09a', 'active': True, 'prefix': 'GHH-', 'suffix': False, 'padding': 4, 'number_increment': 1, 'use_date_range': False})

    action_vals = {'name': 'Update Giá hàng hoá', 'sequence': 5, 'state': 'object_write', 'code': False, 'evaluation_type': 'sequence', 'update_path': 'x_name', 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'x_name'), ('model', '=', 'x_291da0ecd8dc4491b65b085a6adbb09a')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    trigger_field_ids = []
    on_change_field_ids = []

    field_id = env['ir.model.fields'].search([('model_id', '=', 'x_291da0ecd8dc4491b65b085a6adbb09a'), ('name', '=', 'x_name')])
    on_change_field_ids.append(field_id.id)

    auto_vals = {'name': 'default', 'trigger': 'on_change', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    action_vals = {'name': 'Execute Code', 'sequence': 5, 'state': 'code', 'code': 'DISPLAY_SEQUENCE()\n', 'evaluation_type': 'value', 'update_path': False, 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'False'), ('model', '=', 'False')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    model_id = env['ir.model'].search([('model', '=', 'x_2f04e2bc228d49b5b8c910eadba9b63c')])

    trigger_field_ids = []
    on_change_field_ids = []

    auto_vals = {'name': 'ref', 'trigger': 'on_create', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    sequence_id = env['ir.sequence'].create({'name': 'Giá áp dụng', 'implementation': 'standard', 'code': 'x_2f04e2bc228d49b5b8c910eadba9b63c', 'active': True, 'prefix': 'GAD-', 'suffix': False, 'padding': 4, 'number_increment': 1, 'use_date_range': False})

    action_vals = {'name': 'Update Giá áp dụng', 'sequence': 5, 'state': 'object_write', 'code': False, 'evaluation_type': 'sequence', 'update_path': 'x_name', 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'x_name'), ('model', '=', 'x_2f04e2bc228d49b5b8c910eadba9b63c')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    trigger_field_ids = []
    on_change_field_ids = []

    field_id = env['ir.model.fields'].search([('model_id', '=', 'x_2f04e2bc228d49b5b8c910eadba9b63c'), ('name', '=', 'x_name')])
    on_change_field_ids.append(field_id.id)

    auto_vals = {'name': 'default', 'trigger': 'on_change', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    action_vals = {'name': 'Execute Code', 'sequence': 5, 'state': 'code', 'code': 'DISPLAY_SEQUENCE()\n', 'evaluation_type': 'value', 'update_path': False, 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'False'), ('model', '=', 'False')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    model_id = env['ir.model'].search([('model', '=', 'x_df3b7908507d42b2ac2b3a78d2660696')])

    trigger_field_ids = []
    on_change_field_ids = []

    auto_vals = {'name': 'ref', 'trigger': 'on_create', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    sequence_id = env['ir.sequence'].create({'name': 'Hoá đơn', 'implementation': 'standard', 'code': 'x_df3b7908507d42b2ac2b3a78d2660696', 'active': True, 'prefix': 'HOAD-', 'suffix': False, 'padding': 4, 'number_increment': 1, 'use_date_range': False})

    action_vals = {'name': 'Update Hoá đơn', 'sequence': 5, 'state': 'object_write', 'code': False, 'evaluation_type': 'sequence', 'update_path': 'x_name', 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'x_name'), ('model', '=', 'x_df3b7908507d42b2ac2b3a78d2660696')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    model_id = env['ir.model'].search([('model', '=', 'x_9e57e8e385ca48d1b28e1cf1d646b8b6')])

    model_id = env['ir.model'].search([('model', '=', 'x_3719e3f84afb4332a727a7a10419d8f7')])

    trigger_field_ids = []
    on_change_field_ids = []

    auto_vals = {'name': 'ref', 'trigger': 'on_create', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    sequence_id = env['ir.sequence'].create({'name': 'HĐ mua bán', 'implementation': 'standard', 'code': 'x_3719e3f84afb4332a727a7a10419d8f7', 'active': True, 'prefix': 'HDMB-', 'suffix': False, 'padding': 4, 'number_increment': 1, 'use_date_range': False})

    action_vals = {'name': 'Update HĐ mua bán', 'sequence': 5, 'state': 'object_write', 'code': False, 'evaluation_type': 'sequence', 'update_path': 'x_name', 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'x_name'), ('model', '=', 'x_3719e3f84afb4332a727a7a10419d8f7')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    trigger_field_ids = []
    on_change_field_ids = []

    auto_vals = {'name': 'on delete', 'trigger': 'on_unlink', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    action_vals = {'name': 'Execute Code', 'sequence': 5, 'state': 'code', 'code': 'DELETE("Sổ cái kế toán", [("x_loai_chung_tu_id", "=", REF_ID)])\nDELETE("Mua bán hàng hoá", [("x_hd_id", "=", record.id)])\n', 'evaluation_type': 'value', 'update_path': False, 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'False'), ('model', '=', 'False')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    trigger_field_ids = []
    on_change_field_ids = []

    field_id = env['ir.model.fields'].search([('model_id', '=', 'x_3719e3f84afb4332a727a7a10419d8f7'), ('name', '=', 'x_name')])
    on_change_field_ids.append(field_id.id)

    auto_vals = {'name': 'default', 'trigger': 'on_change', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    action_vals = {'name': 'Execute Code', 'sequence': 5, 'state': 'code', 'code': 'DISPLAY_SEQUENCE()\nrecord.write({"x_ngay_thang": datetime.datetime.now()})\n', 'evaluation_type': 'value', 'update_path': False, 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'False'), ('model', '=', 'False')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    model_id = env['ir.model'].search([('model', '=', 'x_48c748e1bb1047d3ad931c4535cc12cf')])

    model_id = env['ir.model'].search([('model', '=', 'x_77605823c2c743a19dfe7674cdbca3bd')])

    trigger_field_ids = []
    on_change_field_ids = []

    auto_vals = {'name': 'ref', 'trigger': 'on_create', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    sequence_id = env['ir.sequence'].create({'name': 'Mua bán hàng hoá', 'implementation': 'standard', 'code': 'x_77605823c2c743a19dfe7674cdbca3bd', 'active': True, 'prefix': 'MBHH-', 'suffix': False, 'padding': 4, 'number_increment': 1, 'use_date_range': False})

    action_vals = {'name': 'Update Mua bán hàng hoá', 'sequence': 5, 'state': 'object_write', 'code': False, 'evaluation_type': 'sequence', 'update_path': 'x_name', 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'x_name'), ('model', '=', 'x_77605823c2c743a19dfe7674cdbca3bd')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    trigger_field_ids = []
    on_change_field_ids = []

    auto_vals = {'name': 'tạo sổ cái kho', 'trigger': 'on_create_or_write', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    action_vals = {'name': 'tính đơn giá', 'sequence': 5, 'state': 'code', 'code': 'if record.x_muc_dich == "Xuất hàng" and not record.x_don_gia:\n    today = datetime.datetime.today().date()\n    x_gad_id = UNIQUE_MODEL("Giá áp dụng").search([\n        ("x_hang_hoa_id", "=", record.x_hang_hoa_id.id), \n        ("x_dsg_id", "=", record.x_dai_ly_id.x_dsg_id.id),\n        ("x_tu_ngay", "<=", today),\n        ("x_den_ngay", ">=", today)\n    ], limit=1)\n\n    record.write({\n        "x_don_gia": x_gad_id.x_don_gia\n    })\n', 'evaluation_type': 'value', 'update_path': False, 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'False'), ('model', '=', 'False')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    action_group_ids = []

    sequence_id = False

    action_vals = {'name': 'tính giá vốn', 'sequence': 6, 'state': 'code', 'code': 'def clean_ledger(ledger):\n    positive = [i for i in ledger if i > 0]\n    negative = sum(1 for i in ledger if i < 0)\n    return positive[negative:]\n\ndef get_rate(ledger, amount):\n    if not amount:\n            return 0\n    left = ledger[:amount]\n    right = ledger[amount:]\n    return sum(left) / amount\n\ndomain = [("x_kho_hang_id", "=", record.x_kho_hang_id.id), ("x_hang_hoa_id", "=", record.x_hang_hoa_id.id)]\n\nif record.x_muc_dich == "Xuất hàng":\n    r = EXPAND_ARRAY("Sổ cái kho", "value:x_gia_von, duplicate:x_sl, before:x_ngay_thang", domain)\n    a = clean_ledger(r)\n\n    rate = get_rate(a, int(record.x_sl))\n    if rate != record.x_gia_von:\n        record.write({"x_gia_von": rate})\nelif record.x_muc_dich == "Nhập hàng":\n    if not record.x_don_gia:\n        record.write({\n            "x_don_gia": record.x_hang_hoa_id.x_gia_von,\n            "x_gia_von": record.x_hang_hoa_id.x_gia_von\n        })\n    else:\n        record.write({"x_gia_von": record.x_don_gia})\n', 'evaluation_type': 'value', 'update_path': False, 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'False'), ('model', '=', 'False')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    action_group_ids = []

    sequence_id = False

    action_vals = {'name': 'Execute Code', 'sequence': 7, 'state': 'code', 'code': 'sck_name = "Sổ cái kho"\nvoucher_type = f"{model._name},{record.id}"\nx_sl = record.x_sl\n\nif record.x_muc_dich == "Xuất hàng":\n    x_sl = -record.x_sl\n\nCREATE_OR_WRITE(sck_name, "x_loai_chung_tu_id, x_kho_hang_id", {\n    "x_loai_chung_tu_id": voucher_type,\n    "x_kho_hang_id": record.x_kho_hang_id.id,\n    "x_ngay_thang": record.x_ngay_thang,\n    "x_sl": x_sl,\n    "x_gia_von": record.x_gia_von,\n    "x_muc_dich": record.x_muc_dich,\n    "x_hang_hoa_id": record.x_hang_hoa_id.id,\n    "x_cong_ty_id": record.x_cong_ty_id.id\n}, "x_kho_hang_id")\n', 'evaluation_type': 'value', 'update_path': False, 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'False'), ('model', '=', 'False')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    trigger_field_ids = []
    on_change_field_ids = []

    auto_vals = {'name': 'tạo sổ cái kế toán', 'trigger': 'on_create_or_write', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    action_vals = {'name': 'Execute Code', 'sequence': 5, 'state': 'code', 'code': 'sck_name = "Sổ cái kế toán"\nvoucher_type = f"{model.x_hd_id._name},{record.x_hd_id.id}"\n\nco_ban = any([r.x_muc_dich == "Xuất hàng" for r in record.x_hd_id.x_items])\nco_mua = any([r.x_muc_dich == "Nhập hàng" for r in record.x_hd_id.x_items])\n\ntong_dinh_gia_ban = sum([r.x_sl * r.x_gia_von for r in record.x_hd_id.x_items if r.x_muc_dich == "Xuất hàng"])\ntong_gia_tri_ban = sum([r.x_sl * r.x_don_gia for r in record.x_hd_id.x_items if r.x_muc_dich == "Xuất hàng"])\ntong_dinh_gia_mua = sum([r.x_sl * r.x_gia_von for r in record.x_hd_id.x_items if r.x_muc_dich == "Nhập hàng"])\ntong_gia_tri_mua = sum([r.x_sl * r.x_don_gia for r in record.x_hd_id.x_items if r.x_muc_dich == "Nhập hàng"])\n\nCREATE_OR_WRITE(sck_name, "x_loai_chung_tu_id, x_account_type, x_ghi_chu", {\n    "x_loai_chung_tu_id": voucher_type,\n    "x_ghi_chu": "Xuất hàng",\n    "x_account_type": "Stock",\n    "x_tai_khoan_id": record.x_hd_id.x_cong_ty_id.x_tk_kho_id.id,\n    "x_tk_doi_ung": record.x_hd_id.x_cong_ty_id.x_tk_chi_phi_id.x_name,\n\n    "x_ngay_thang": record.x_hd_id.x_ngay_thang,\n    "x_credit": tong_dinh_gia_ban,\n    "x_dai_ly_id": record.x_hd_id.x_dai_ly_id.id,\n    "x_cong_ty_id": record.x_hd_id.x_cong_ty_id.id\n}, "x_account_type", co_ban)\n\nCREATE_OR_WRITE(sck_name, "x_loai_chung_tu_id, x_account_type, x_ghi_chu", {\n    "x_loai_chung_tu_id": voucher_type,\n    "x_account_type": "Cost of Goods Sold",\n    "x_ghi_chu": "Cost of Goods Sold",\n    "x_tai_khoan_id": record.x_hd_id.x_cong_ty_id.x_tk_chi_phi_id.id,\n    "x_tk_doi_ung": record.x_hd_id.x_cong_ty_id.x_tk_kho_id.x_name,\n\n    "x_ngay_thang": record.x_hd_id.x_ngay_thang,\n    "x_debit": tong_dinh_gia_ban,\n    "x_dai_ly_id": record.x_hd_id.x_dai_ly_id.id,\n    "x_cong_ty_id": record.x_hd_id.x_cong_ty_id.id\n}, "x_account_type", co_ban)\n\nCREATE_OR_WRITE(sck_name, "x_loai_chung_tu_id, x_account_type, x_ghi_chu", {\n    "x_loai_chung_tu_id": voucher_type,\n    "x_account_type": "Receivable",\n    "x_ghi_chu": "Receivable",\n    "x_tai_khoan_id": record.x_hd_id.x_cong_ty_id.x_tk_phai_thu_id.id,\n    "x_tk_doi_ung": record.x_hd_id.x_cong_ty_id.x_tk_doanh_thu_id.x_name,\n\n    "x_ngay_thang": record.x_hd_id.x_ngay_thang,\n    "x_debit": tong_gia_tri_ban,\n    "x_dai_ly_id": record.x_hd_id.x_dai_ly_id.id,\n    "x_cong_ty_id": record.x_hd_id.x_cong_ty_id.id\n}, "x_account_type", co_ban)\n\nCREATE_OR_WRITE(sck_name, "x_loai_chung_tu_id, x_root_type, x_ghi_chu", {\n    "x_loai_chung_tu_id": voucher_type,\n    "x_root_type": "Income",\n    "x_ghi_chu": "Income",\n    "x_tai_khoan_id": record.x_hd_id.x_cong_ty_id.x_tk_doanh_thu_id.id,\n    "x_tk_doi_ung": record.x_hd_id.x_cong_ty_id.x_tk_phai_thu_id.x_name,\n\n    "x_ngay_thang": record.x_hd_id.x_ngay_thang,\n    "x_credit": tong_gia_tri_ban,\n    "x_dai_ly_id": record.x_hd_id.x_dai_ly_id.id,\n    "x_cong_ty_id": record.x_hd_id.x_cong_ty_id.id\n}, "x_root_type", co_ban)\n\nCREATE_OR_WRITE(sck_name, "x_loai_chung_tu_id, x_account_type, x_ghi_chu", {\n    "x_loai_chung_tu_id": voucher_type,\n    "x_ghi_chu": "Nhập hàng",\n    "x_account_type": "Stock",\n    "x_tai_khoan_id": record.x_hd_id.x_cong_ty_id.x_tk_kho_id.id,\n    "x_tk_doi_ung": record.x_hd_id.x_cong_ty_id.x_tk_phai_tra_id.x_name,\n\n    "x_ngay_thang": record.x_hd_id.x_ngay_thang,\n    "x_debit": tong_dinh_gia_mua,\n    "x_dai_ly_id": record.x_hd_id.x_dai_ly_id.id,\n    "x_cong_ty_id": record.x_hd_id.x_cong_ty_id.id\n}, "x_account_type", co_mua)\n\nCREATE_OR_WRITE(sck_name, "x_loai_chung_tu_id, x_account_type, x_ghi_chu", {\n    "x_loai_chung_tu_id": voucher_type,\n    "x_account_type": "Payable",\n    "x_ghi_chu": "Payable",\n    "x_tai_khoan_id": record.x_hd_id.x_cong_ty_id.x_tk_phai_tra_id.id,\n    "x_tk_doi_ung": record.x_hd_id.x_cong_ty_id.x_tk_kho_id.x_name,\n\n    "x_ngay_thang": record.x_hd_id.x_ngay_thang,\n    "x_credit": tong_dinh_gia_mua,\n    "x_dai_ly_id": record.x_hd_id.x_dai_ly_id.id,\n    "x_cong_ty_id": record.x_hd_id.x_cong_ty_id.id\n}, "x_account_type", co_mua)\n', 'evaluation_type': 'value', 'update_path': False, 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'False'), ('model', '=', 'False')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    trigger_field_ids = []
    on_change_field_ids = []

    auto_vals = {'name': 'on delete', 'trigger': 'on_unlink', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    action_vals = {'name': 'Execute Code', 'sequence': 5, 'state': 'code', 'code': 'DELETE("Sổ cái kho", [("x_loai_chung_tu_id", "=", REF_ID)])\nDELETE("Nhật ký thanh toán", [("x_mbhh_id", "=", record.id)])\n', 'evaluation_type': 'value', 'update_path': False, 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'False'), ('model', '=', 'False')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    action_group_ids = []

    sequence_id = False

    action_vals = {'name': 'Thanh toán', 'sequence': 5, 'state': 'code', 'code': '# env.context.update({"x_mbhh_id": record.id})\n\naction2 = ACT_WINDOW("Thanh toán")\naction2.write({\n    "context": {\n    "x_hd_id": record.x_hd_id.id,\n    }\n})\naction = action2.open()', 'evaluation_type': 'value', 'update_path': False, 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'False'), ('model', '=', 'False')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if True:
        binding_model_id = env['ir.model'].search([('model', '=', 'x_77605823c2c743a19dfe7674cdbca3bd')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    model_id = env['ir.model'].search([('model', '=', 'x_7076d1049e954d7985d7e2cd445e5b20')])

    trigger_field_ids = []
    on_change_field_ids = []

    auto_vals = {'name': 'ref', 'trigger': 'on_create', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    sequence_id = env['ir.sequence'].create({'name': 'Nhật ký thanh toán', 'implementation': 'standard', 'code': 'x_7076d1049e954d7985d7e2cd445e5b20', 'active': True, 'prefix': 'NKTT-', 'suffix': False, 'padding': 4, 'number_increment': 1, 'use_date_range': False})

    action_vals = {'name': 'Update Nhật ký thanh toán', 'sequence': 5, 'state': 'object_write', 'code': False, 'evaluation_type': 'sequence', 'update_path': 'x_name', 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'x_name'), ('model', '=', 'x_7076d1049e954d7985d7e2cd445e5b20')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    trigger_field_ids = []
    on_change_field_ids = []

    field_id = env['ir.model.fields'].search([('model_id', '=', 'x_7076d1049e954d7985d7e2cd445e5b20'), ('name', '=', 'x_name')])
    on_change_field_ids.append(field_id.id)

    auto_vals = {'name': 'default', 'trigger': 'on_change', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    action_vals = {'name': 'Execute Code', 'sequence': 5, 'state': 'code', 'code': 'record.write({"x_ngay_thang": datetime.datetime.now()})', 'evaluation_type': 'value', 'update_path': False, 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'False'), ('model', '=', 'False')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    trigger_field_ids = []
    on_change_field_ids = []

    auto_vals = {'name': 'tạo sổ cái kế toán', 'trigger': 'on_create_or_write', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    action_vals = {'name': 'Execute Code', 'sequence': 5, 'state': 'code', 'code': 'sck_name = "Sổ cái kế toán"\nvoucher_type = f"{model._name},{record.id}"\n\nx_tk_doi_ung = record.x_cong_ty_id.x_tk_tien_mat_id.x_name\nx_tk_doi_ung_tt = record.x_cong_ty_id.x_tk_phai_thu_id.x_name\nx_debit_tt = record.x_thanh_toan\nx_credit_tt = 0\n\nif record.x_loai_thanh_toan == "Ngân hàng":\n    x_tk_doi_ung = record.x_cong_ty_id.x_tk_ngan_hang_id.x_name\nif record.x_mbhh_id.x_muc_dich == "Nhập hàng":\n    x_tk_doi_ung_tt = record.x_cong_ty_id.x_tk_phai_tra_id.x_name\n    x_debit_tt = 0\n    x_credit_tt = record.x_thanh_toan\n\nCREATE_OR_WRITE(sck_name, "x_loai_chung_tu_id, x_account_type, x_ghi_chu", {\n    "x_loai_chung_tu_id": voucher_type,\n    "x_account_type": "Receivable",\n    "x_ghi_chu": "Receivable",\n    "x_tai_khoan_id": record.x_mbhh_id.x_cong_ty_id.x_tk_phai_thu_id.id,\n    "x_tk_doi_ung": x_tk_doi_ung,\n\n    "x_ngay_thang": record.x_mbhh_id.x_ngay_thang,\n    "x_credit": record.x_thanh_toan,\n    "x_dai_ly_id": record.x_mbhh_id.x_dai_ly_id.id,\n    "x_cong_ty_id": record.x_mbhh_id.x_cong_ty_id.id\n}, "x_account_type", record.x_mbhh_id.x_muc_dich == "Xuất hàng")\n\nCREATE_OR_WRITE(sck_name, "x_loai_chung_tu_id, x_account_type, x_ghi_chu", {\n    "x_loai_chung_tu_id": voucher_type,\n    "x_account_type": "Payable",\n    "x_ghi_chu": "Payable",\n    "x_tai_khoan_id": record.x_mbhh_id.x_cong_ty_id.x_tk_phai_tra_id.id,\n    "x_tk_doi_ung": x_tk_doi_ung,\n\n    "x_ngay_thang": record.x_mbhh_id.x_ngay_thang,\n    "x_debit": record.x_thanh_toan,\n    "x_dai_ly_id": record.x_mbhh_id.x_dai_ly_id.id,\n    "x_cong_ty_id": record.x_mbhh_id.x_cong_ty_id.id\n}, "x_account_type", record.x_mbhh_id.x_muc_dich == "Nhập hàng")\n\nCREATE_OR_WRITE(sck_name, "x_loai_chung_tu_id, x_account_type, x_ghi_chu", {\n    "x_loai_chung_tu_id": voucher_type,\n    "x_account_type": "Cash",\n    "x_ghi_chu": "Cash",\n    "x_tai_khoan_id": record.x_mbhh_id.x_cong_ty_id.x_tk_tien_mat_id.id,\n    "x_tk_doi_ung": x_tk_doi_ung_tt,\n\n    "x_ngay_thang": record.x_mbhh_id.x_ngay_thang,\n    "x_debit": x_debit_tt,\n    "x_credit": x_credit_tt,\n    "x_dai_ly_id": record.x_mbhh_id.x_dai_ly_id.id,\n    "x_cong_ty_id": record.x_mbhh_id.x_cong_ty_id.id\n}, "x_account_type", record.x_loai_thanh_toan == "Tiền mặt")\n\nCREATE_OR_WRITE(sck_name, "x_loai_chung_tu_id, x_account_type, x_ghi_chu", {\n    "x_loai_chung_tu_id": voucher_type,\n    "x_account_type": "Bank",\n    "x_ghi_chu": "Bank",\n    "x_tai_khoan_id": record.x_mbhh_id.x_cong_ty_id.x_tk_ngan_hang_id.id,\n    "x_tk_doi_ung": x_tk_doi_ung_tt,\n\n    "x_ngay_thang": record.x_mbhh_id.x_ngay_thang,\n    "x_debit": x_debit_tt,\n    "x_credit": x_credit_tt,\n    "x_dai_ly_id": record.x_mbhh_id.x_dai_ly_id.id,\n    "x_cong_ty_id": record.x_mbhh_id.x_cong_ty_id.id\n}, "x_account_type", record.x_loai_thanh_toan == "Ngân hàng")\n', 'evaluation_type': 'value', 'update_path': False, 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'False'), ('model', '=', 'False')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    trigger_field_ids = []
    on_change_field_ids = []

    auto_vals = {'name': 'on delete', 'trigger': 'on_unlink', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    action_vals = {'name': 'Execute Code', 'sequence': 5, 'state': 'code', 'code': 'DELETE("Sổ cái kho", [("x_loai_chung_tu_id", "=", REF_ID)])\nDELETE("Sổ cái kế toán", [("x_loai_chung_tu_id", "=", REF_ID)])\n', 'evaluation_type': 'value', 'update_path': False, 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'False'), ('model', '=', 'False')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    model_id = env['ir.model'].search([('model', '=', 'x_c90f6c65498d4983bdf0d7371f40618b')])

    trigger_field_ids = []
    on_change_field_ids = []

    auto_vals = {'name': 'ref', 'trigger': 'on_create', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    sequence_id = env['ir.sequence'].create({'name': 'Phiếu kho', 'implementation': 'standard', 'code': 'x_c90f6c65498d4983bdf0d7371f40618b', 'active': True, 'prefix': 'PHK-', 'suffix': False, 'padding': 4, 'number_increment': 1, 'use_date_range': False})

    action_vals = {'name': 'Update Phiếu kho', 'sequence': 5, 'state': 'object_write', 'code': False, 'evaluation_type': 'sequence', 'update_path': 'x_name', 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'x_name'), ('model', '=', 'x_c90f6c65498d4983bdf0d7371f40618b')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    trigger_field_ids = []
    on_change_field_ids = []

    auto_vals = {'name': 'on delete', 'trigger': 'on_unlink', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    action_vals = {'name': 'Execute Code', 'sequence': 5, 'state': 'code', 'code': 'DELETE("Sổ cái kế toán", [("x_loai_chung_tu_id", "=", REF_ID)])\nDELETE("Xuất nhập kho", [("x_phieu_kho_id", "=", record.id)])\n', 'evaluation_type': 'value', 'update_path': False, 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'False'), ('model', '=', 'False')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    trigger_field_ids = []
    on_change_field_ids = []

    field_id = env['ir.model.fields'].search([('model_id', '=', 'x_c90f6c65498d4983bdf0d7371f40618b'), ('name', '=', 'x_name')])
    on_change_field_ids.append(field_id.id)

    auto_vals = {'name': 'set default', 'trigger': 'on_change', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    action_vals = {'name': 'Execute Code', 'sequence': 5, 'state': 'code', 'code': 'DISPLAY_SEQUENCE()\nrecord.write({"x_ngay_thang": datetime.datetime.now()})\n', 'evaluation_type': 'value', 'update_path': False, 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'False'), ('model', '=', 'False')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    model_id = env['ir.model'].search([('model', '=', 'x_c68ffd06f8144e7d9a4e5ccc52fd9a93')])

    trigger_field_ids = []
    on_change_field_ids = []

    auto_vals = {'name': 'ref', 'trigger': 'on_create', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    sequence_id = env['ir.sequence'].create({'name': 'Sổ cái kho', 'implementation': 'standard', 'code': 'x_c68ffd06f8144e7d9a4e5ccc52fd9a93', 'active': True, 'prefix': 'SCK-', 'suffix': False, 'padding': 4, 'number_increment': 1, 'use_date_range': False})

    action_vals = {'name': 'Update Sổ cái kho', 'sequence': 5, 'state': 'object_write', 'code': False, 'evaluation_type': 'sequence', 'update_path': 'x_name', 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'x_name'), ('model', '=', 'x_c68ffd06f8144e7d9a4e5ccc52fd9a93')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    action_group_ids = []

    sequence_id = False

    action_vals = {'name': 'Tạo báo cáo', 'sequence': 5, 'state': 'code', 'code': 'action = ACT_WINDOW("Model sổ cái").open()', 'evaluation_type': 'value', 'update_path': False, 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'False'), ('model', '=', 'False')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if True:
        binding_model_id = env['ir.model'].search([('model', '=', 'x_c68ffd06f8144e7d9a4e5ccc52fd9a93')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    model_id = env['ir.model'].search([('model', '=', 'x_07c472ed342844baa780906b13dba020')])

    trigger_field_ids = []
    on_change_field_ids = []

    auto_vals = {'name': 'ref', 'trigger': 'on_create', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    sequence_id = env['ir.sequence'].create({'name': 'Sổ cái kế toán', 'implementation': 'standard', 'code': 'x_07c472ed342844baa780906b13dba020', 'active': True, 'prefix': 'SCKT-', 'suffix': False, 'padding': 4, 'number_increment': 1, 'use_date_range': False})

    action_vals = {'name': 'Update Sổ cái kế toán', 'sequence': 5, 'state': 'object_write', 'code': False, 'evaluation_type': 'sequence', 'update_path': 'x_name', 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'x_name'), ('model', '=', 'x_07c472ed342844baa780906b13dba020')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    trigger_field_ids = []
    on_change_field_ids = []

    auto_vals = {'name': 'thiết lập bút toán điều chỉnh chứng từ', 'trigger': 'on_create_or_write', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    action_vals = {'name': 'Execute Code', 'sequence': 5, 'state': 'code', 'code': 'ref_id = REF(record.x_bt_dc_id._name, record.x_bt_dc_id.id)\nif record.x_bt_dc_id:\n    record.write({"x_loai_chung_tu_id": ref_id})\n', 'evaluation_type': 'value', 'update_path': False, 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'False'), ('model', '=', 'False')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    trigger_field_ids = []
    on_change_field_ids = []

    field_id = env['ir.model.fields'].search([('model_id', '=', 'x_07c472ed342844baa780906b13dba020'), ('name', '=', 'x_name')])
    on_change_field_ids.append(field_id.id)

    auto_vals = {'name': 'default', 'trigger': 'on_change', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    action_vals = {'name': 'Execute Code', 'sequence': 5, 'state': 'code', 'code': 'DISPLAY_SEQUENCE()\n', 'evaluation_type': 'value', 'update_path': False, 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'False'), ('model', '=', 'False')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    model_id = env['ir.model'].search([('model', '=', 'x_500b7a5ea68541cb82fc5cc4e7be7c6a')])

    model_id = env['ir.model'].search([('model', '=', 'x_f0637b5ecea4413289b8fee8086af2e0')])

    trigger_field_ids = []
    on_change_field_ids = []

    auto_vals = {'name': 'ref', 'trigger': 'on_create', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    sequence_id = env['ir.sequence'].create({'name': 'Xuất nhập kho', 'implementation': 'standard', 'code': 'x_f0637b5ecea4413289b8fee8086af2e0', 'active': True, 'prefix': 'XNK-', 'suffix': False, 'padding': 4, 'number_increment': 1, 'use_date_range': False})

    action_vals = {'name': 'Update Xuất nhập kho', 'sequence': 5, 'state': 'object_write', 'code': False, 'evaluation_type': 'sequence', 'update_path': 'x_name', 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'x_name'), ('model', '=', 'x_f0637b5ecea4413289b8fee8086af2e0')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    trigger_field_ids = []
    on_change_field_ids = []

    auto_vals = {'name': 'tạo sổ cái kho', 'trigger': 'on_create_or_write', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    action_vals = {'name': 'tính giá vốn', 'sequence': 6, 'state': 'code', 'code': 'def clean_ledger(ledger):\n    positive = [i for i in ledger if i > 0]\n    negative = sum(1 for i in ledger if i < 0)\n    return positive[negative:]\n\ndef get_rate(ledger, amount):\n    if not amount:\n            return 0\n    left = ledger[:amount]\n    right = ledger[amount:]\n    return sum(left) / amount\n\ndomain = [("x_kho_hang_id", "=", record.x_kho_nguon_id.id), ("x_hang_hoa_id", "=", record.x_hang_hoa_id.id)]\n\nif record.x_muc_dich == "Xuất hàng":\n    r = EXPAND_ARRAY("Sổ cái kho", "value:x_gia_von, duplicate:x_sl, before:x_ngay_thang", domain)\n    a = clean_ledger(r)\n\n    rate = get_rate(a, int(record.x_sl))\n    if rate != record.x_gia_von:\n        record.write({"x_gia_von": rate})\nelif record.x_muc_dich == "Nhập hàng" and not record.x_gia_von:\n    record.write({"x_gia_von": record.x_hang_hoa_id.x_gia_von})\n', 'evaluation_type': 'value', 'update_path': False, 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'False'), ('model', '=', 'False')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    action_group_ids = []

    sequence_id = False

    action_vals = {'name': 'Execute Code', 'sequence': 8, 'state': 'code', 'code': 'sck_name = "Sổ cái kho"\n\nCREATE_OR_WRITE(sck_name, "x_loai_chung_tu_id, x_kho_hang_id, x_ghi_chu", {\n    "x_loai_chung_tu_id": REF_ID,\n    "x_kho_hang_id": record.x_kho_dich_id.id,\n    "x_ghi_chu": "Kho đích",\n    "x_ngay_thang": record.x_ngay_thang,\n    "x_sl": record.x_sl,\n    "x_gia_von": record.x_gia_von,\n    "x_muc_dich": record.x_muc_dich,\n    "x_hang_hoa_id": record.x_hang_hoa_id.id,\n    "x_cong_ty_id": record.x_cong_ty_id.id\n}, "x_kho_hang_id")\n\nCREATE_OR_WRITE(sck_name, "x_loai_chung_tu_id, x_kho_hang_id, x_ghi_chu", {\n    "x_loai_chung_tu_id": REF_ID,\n    "x_kho_hang_id": record.x_kho_nguon_id.id,\n    "x_ghi_chu": "Kho nguồn",\n    "x_ngay_thang": record.x_ngay_thang,\n    "x_sl": -record.x_sl,\n    "x_gia_von": record.x_gia_von,\n    "x_muc_dich": record.x_muc_dich,\n    "x_hang_hoa_id": record.x_hang_hoa_id.id,\n    "x_cong_ty_id": record.x_cong_ty_id.id\n}, "x_kho_hang_id", record.x_muc_dich == "Xuất hàng")\n', 'evaluation_type': 'value', 'update_path': False, 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'False'), ('model', '=', 'False')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    trigger_field_ids = []
    on_change_field_ids = []

    auto_vals = {'name': 'tạo sổ cái kế toán', 'trigger': 'on_create_or_write', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    action_vals = {'name': 'Execute Code', 'sequence': 5, 'state': 'code', 'code': 'sck_name = "Sổ cái kế toán"\n\ntong_dinh_gia = sum([r.x_sl * r.x_gia_von for r in record.x_phieu_kho_id.x_items])\nreference_id = REF(record.x_phieu_kho_id._name, record.x_phieu_kho_id.id)\nnhap_hang = record.x_muc_dich == "Nhập hàng"\n\nCREATE_OR_WRITE(sck_name, "x_loai_chung_tu_id, x_account_type, x_ghi_chu", {\n    "x_loai_chung_tu_id": reference_id,\n    "x_tai_khoan_id": record.x_phieu_kho_id.x_cong_ty_id.x_tk_kho_id.id,\n    "x_account_type": "Stock",\n    "x_ghi_chu": "Stock",\n    "x_ngay_thang": record.x_phieu_kho_id.x_ngay_thang,\n    "x_debit": tong_dinh_gia,\n    "x_tk_doi_ung": record.x_phieu_kho_id.x_cong_ty_id.x_tk_dieu_chinh_id.x_name,\n    "x_cong_ty_id": record.x_phieu_kho_id.x_cong_ty_id.id\n}, "x_account_type", nhap_hang)\n\nCREATE_OR_WRITE(sck_name, "x_loai_chung_tu_id, x_account_type, x_ghi_chu", {\n    "x_loai_chung_tu_id": reference_id,\n    "x_tai_khoan_id": record.x_phieu_kho_id.x_cong_ty_id.x_tk_dieu_chinh_id.id,\n    "x_account_type": "Stock Adjustment",\n    "x_ghi_chu": "Stock Adjustment",\n    "x_ngay_thang": record.x_phieu_kho_id.x_ngay_thang,\n    "x_credit": tong_dinh_gia,\n    "x_tk_doi_ung": record.x_phieu_kho_id.x_cong_ty_id.x_tk_kho_id.x_name,\n    "x_cong_ty_id": record.x_phieu_kho_id.x_cong_ty_id.id\n}, "x_account_type", nhap_hang)\n', 'evaluation_type': 'value', 'update_path': False, 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'False'), ('model', '=', 'False')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    trigger_field_ids = []
    on_change_field_ids = []

    auto_vals = {'name': 'on delete', 'trigger': 'on_unlink', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    action_vals = {'name': 'Execute Code', 'sequence': 5, 'state': 'code', 'code': 'DELETE("Sổ cái kho", [("x_loai_chung_tu_id", "=", REF_ID)])\n', 'evaluation_type': 'value', 'update_path': False, 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'False'), ('model', '=', 'False')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    action_group_ids = []

    sequence_id = False

    action_vals = {'name': 'Execute Code', 'sequence': 5, 'state': 'code', 'code': False, 'evaluation_type': 'value', 'update_path': False, 'value': False, 'binding_type': 'action'}
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

    model_id = env['ir.model'].search([('model', '=', 'x_47586e8c7d9744c3a1f1992a10a30b16')])

    model_id = env['ir.model'].search([('model', '=', 'x_model_so_cai')])

    action_group_ids = []

    sequence_id = False

    action_vals = {'name': 'ok', 'sequence': 5, 'state': 'code', 'code': 'sck_id = UNIQUE_MODEL("Sổ cái kho")\nx_nk_mb_id = UNIQUE_MODEL("Mua bán hàng hoá")\n\ntdk = sck_id.search([("x_ngay_thang", "<", record.x_tu_ngay)])\nttk = sck_id.search([\n    ("x_ngay_thang", ">=", record.x_tu_ngay), ("x_ngay_thang", "<=", record.x_den_ngay), ("x_loai_chung_tu_id", "not like", x_nk_mb_id._name + ",")\n])\nttk2 = sck_id.search([\n    ("x_ngay_thang", ">=", record.x_tu_ngay), \n    ("x_ngay_thang", "<=", record.x_den_ngay), \n    ("x_loai_chung_tu_id", "like", x_nk_mb_id._name + ","),\n    ("x_sl", ">", 0)\n])\nxbtk = sck_id.search([\n    ("x_ngay_thang", ">=", record.x_tu_ngay), \n    ("x_ngay_thang", "<=", record.x_den_ngay), \n    ("x_loai_chung_tu_id", "like", x_nk_mb_id._name + ","),\n    ("x_sl", "<", 0)\n])\nleft = sck_id.search([("x_ngay_thang", ">", record.x_den_ngay)])\nleft.write({"x_loai_ky": ""})\ntdk.write({"x_loai_ky": "Tồn đầu kỳ"})\nttk.write({"x_loai_ky": "Nhập trong kỳ"})\nttk2.write({"x_loai_ky": "Nhập trong kỳ"})\nxbtk.write({"x_loai_ky": "Xuất bán trong kỳ"})\n\nact = ACT_WINDOW("Báo cáo tổng hợp")\nact.write({"name": f"Báo cáo kho ngày {record.x_tu_ngay} đến ngày {record.x_den_ngay}"})\naction = act.open()', 'evaluation_type': 'value', 'update_path': False, 'value': False, 'binding_type': 'action'}
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

    model_id = env['ir.model'].search([('model', '=', 'x_model_thanh_toan')])

    trigger_field_ids = []
    on_change_field_ids = []

    field_id = env['ir.model.fields'].search([('model_id', '=', 'x_model_thanh_toan'), ('name', '=', 'x_name')])
    on_change_field_ids.append(field_id.id)

    auto_vals = {'name': 'default', 'trigger': 'on_change', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    action_vals = {'name': 'Execute Code', 'sequence': 5, 'state': 'code', 'code': 'record.write({\n    "x_ngay_thang": datetime.datetime.now(),\n    "x_loai_thanh_toan": "Tiền mặt",\n    "x_chuc_nang": "Xoá cũ tạo mới"\n})', 'evaluation_type': 'value', 'update_path': False, 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'False'), ('model', '=', 'False')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    trigger_field_ids = []
    on_change_field_ids = []

    auto_vals = {'name': 'ref', 'trigger': 'on_create', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    sequence_id = env['ir.sequence'].create({'name': 'Model thanh toán', 'implementation': 'standard', 'code': 'x_model_thanh_toan', 'active': True, 'prefix': 'MDTT-', 'suffix': False, 'padding': 4, 'number_increment': 1, 'use_date_range': False})

    action_vals = {'name': 'Update model thanh toan', 'sequence': 5, 'state': 'object_write', 'code': False, 'evaluation_type': 'sequence', 'update_path': 'x_name', 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'x_name'), ('model', '=', 'x_model_thanh_toan')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    action_group_ids = []

    sequence_id = False

    action_vals = {'name': 'ok', 'sequence': 5, 'state': 'code', 'code': 'if record.x_chuc_nang == "Thêm tiền":\n    raise UserError("Chưa triển khai chức năng này!")\n\nx_hd_id = UNIQUE_MODEL("HĐ mua bán").browse(env.context.get("x_hd_id"))\nx_hd_id.x_items.x_nk_tt_ids.unlink()\n\ntotal = record.x_thanh_toan\n\nfor nk in x_hd_id.x_items:\n    if total >= nk.x_thanh_tien:\n        CREATE("Nhật ký thanh toán", {\n            "x_ngay_thang": record.x_ngay_thang,\n            "x_loai_thanh_toan": record.x_loai_thanh_toan,\n            "x_thanh_toan": nk.x_thanh_tien,\n            "x_mbhh_id": nk.id\n        })\n        total -= nk.x_thanh_tien\n    else:\n        CREATE("Nhật ký thanh toán", {\n            "x_ngay_thang": record.x_ngay_thang,\n            "x_loai_thanh_toan": record.x_loai_thanh_toan,\n            "x_thanh_toan": total,\n            "x_mbhh_id": nk.id\n        })\n', 'evaluation_type': 'value', 'update_path': False, 'value': False, 'binding_type': 'action'}
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
    rec = env['erp.custom.app'].search([('uuid', '=', 'uuid_ffa9efc5c0074f499c2e5e84dba64dd4')], limit=1)

    if rec:
        rec.unlink()
