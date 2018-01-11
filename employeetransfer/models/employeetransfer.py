from datetime import datetime,date, timedelta
from odoo import models, fields, api, _
from odoo.exceptions import Warning

class employeetransfer(models.Model):
    _name = 'employee.transfer'
    _description = "Employees Transfer"
    _rec_name = 'employee_id'

    @api.multi
    def request_set(self):
        self.state = 'draft'

    @api.multi
    def exit_cancel(self):
        self.state = 'cancel'

    @api.multi
    def get_confirm(self):
        self.state = 'confirm'
        act_obj = self.env['hr.employee'].search([('id', '=', self.employee_id.id)],limit=1)
        self.from_department_id = act_obj.department_id
        act_obj1 = self.env['hr.employee']
        act_obj1.search([('id', '=', self.employee_id.id)]).write({'department_id': '%s' % self.to_department_id.id})

    @api.multi
    def get_apprv_dept_manager(self):
        self.state = 'approved'

    @api.multi
    def get_apprv_hr_manager(self):
        self.state = 'approved'

    @api.multi
    def get_apprv_general_manager(self):
        self.state = 'approved'

    @api.multi
    def get_done(self):
        self.state = 'done'

    @api.multi
    def get_reject(self):
        self.state = 'reject'


    state = fields.Selection(selection=[('draft', 'draft'), \
                                        ('confirm', 'Confirmed'), \
                                        ('approved', 'Approved'), \
                                        ('reject', 'Rejected'), \
                                        ('cancel', 'Cancelled')], \
                             string='State', default='draft', track_visibility='onchange')


    @api.model
    def _get_default_name(self):
        return self.env['ir.sequence'].next_by_code('employee.transfer')

    name = fields.Char('Transfer ID',required=True,default=_get_default_name,track_visibility='onchange',readonly='1')
    request_date = fields.Date('Request Date',default=fields.datetime.now())

    requested_by = fields.Many2one('res.users','Requested by',required=True,track_visibility='onchange')
    employee_id = fields.Many2one('hr.employee', required=True, string="Employee")
    from_department_id = fields.Many2one('hr.department', string='From Department',readonly=True, store=True)
    job_id = fields.Many2one(related='employee_id.job_id',string='Job Title', type='many2one', relation='hr.department',readonly=True, store=True)
    employee_number = fields.Char(related='employee_id.employee_number',string='Employee Number',readonly = True,store = True)

    transfer_date = fields.Date('Transfer Date')
    to_department_id = fields.Many2one('hr.department', string='To Department')
    transfer_note = fields.Text('Transfer note')






class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    transfer_count = fields.Integer(compute='_transfer_count', string='# Transfer')
    @api.multi
    def _transfer_count(self):
        for each in self:
            transfer_ids = self.env['employee.transfer'].search([('employee_id', '=', each.id)])
            each.transfer_count = len(transfer_ids)

    @api.multi
    def transfer_view(self):
        self.ensure_one()
        domain = [
            ('employee_id', '=', self.id)]
        return {
            'name': _('Employee Transfer'),
            'domain': domain,
            'res_model': 'employee.transfer',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'tree,form',
            'view_type': 'form',
            'help': _('''<p class="oe_view_nocontent_create">
                           Click to Create for New Documents
                        </p>'''),
            'limit': 80,
            'context': "{'default_employee_id': %s}" % self.id
        }









