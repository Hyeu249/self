from odoo import models, fields, api
from odoo.exceptions import ValidationError

class BackupDetail(models.Model):
    _name = "backup.detail"

    path = fields.Char(
        string="Path",
        required=True,
        readonly=True
    )
    backup_operation_id = fields.Many2one('backup.operation')

class BackupOperation(models.Model):
    _name = "backup.operation"
    _description = "Backup Operation"

    retention = fields.Integer("Backup retention count", required=True, default=7)
    nextcall = fields.Datetime("Backup starting time", default=fields.Datetime.now)
    interval_number = fields.Integer("Interval Number", required=True)
    interval_type = fields.Selection([
        ('minutes', 'Minutes'),
        ('hours', 'Hours'),
        ('days', 'Days'),
        ('weeks', 'Weeks'),
        ('months', 'Months')],
        required=True,
        string="Interval Unit", 
        default='days'
    )
    status = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('running', 'Running'),
        ('cancel', 'Cancel')],
        required=True,
        string="Status", 
        default='draft'
    )
    detail_ids = fields.One2many(
        'backup.detail', 
        'backup_operation_id',
        string="Backup File",
    )

    def backup_db(self):
        self.ensure_one()
        from odoo.service.db import dump_db
        import os
        from datetime import datetime, timezone
        import pytz

        tz = pytz.timezone('Asia/Ho_Chi_Minh')
        now_local = datetime.now(timezone.utc).astimezone(tz).replace(microsecond=0)

        backup_path="/opt/odoo19/backups"
        backup_format="zip"
        filestore=True
        dbname = self.env.cr.dbname
        os.makedirs(backup_path, exist_ok=True)
        file_path = os.path.join(backup_path, f"{dbname}_{now_local.strftime('%d-%m-%Y_%H-%M-%S')}.{backup_format}")
        with open(file_path, "wb") as f:
            dump_db(dbname, f, backup_format, filestore)
        
        self.detail_ids.create({
            "path": file_path, 
            "backup_operation_id": self.id
        })
        return file_path
