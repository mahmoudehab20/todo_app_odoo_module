from odoo import models,fields,api
from datetime import datetime,timedelta
import random,string

class TodoTask(models.Model):
    _name="todo.task"
    _description="Todo Task"
    _inherit = ['mail.thread','mail.activity.mixin']
    status_selection=[('draft','Draft'),
                    ('in progress','In Progress'),
                    ('completed','Completed'),
                    ('close','Close')]

    ref=fields.Char(default='new',readonly=True)
    name=fields.Char('Task Name')
    description=fields.Text()
    due_date=fields.Date()
    status=fields.Selection(status_selection,default='draft')
    assign_to_id=fields.Many2one('res.partner')
    estimated_time=fields.Integer('Estimated Time(hr)')
    lines_ids=fields.One2many('time.sheet','todo_task')
    active=fields.Boolean(default=True)
    islate=fields.Boolean(default=False)


    @api.model
    def create(self,vals):
        res=super(TodoTask,self).create(vals)
        if res.ref=='new':
            res.ref=res.env['ir.sequence'].next_by_code('task_seq')
        return res


    def check_due_date(self):
        task_id=self.search([])
        for rec in task_id:
            if rec.due_date and rec.due_date < fields.Date.today():
                rec.islate=True

    def action_new(self):
        for rec in self:
            rec.status='draft'

    def action_in_progress(self):
        for rec in self:
            rec.status='in progress'

    def action_completed(self):
        for rec in self:
            rec.status='completed'

    def action_close(self):
        for rec in self:
            rec.status='close'

class TimeSheet(models.Model):
    _name='time.sheet'

    description=fields.Char()
    date=fields.Date()
    time=fields.Integer() 
    todo_task=fields.Many2one('todo.task')


class Token(models.Model):
    _name='token'
    _description='Token'

    token=fields.Char(default='new',readonly=True)
    estimated_date=fields.Datetime(default=datetime.now()+timedelta(hours=2))

    @api.model
    def create(self,vals):
        res=super(Token,self).create(vals)
        if res.token=='new':
            res.token=''.join(random.choices(string.ascii_letters,k=10))
        return res

    def check_token_date(self):
        token_id=self.search([])
        for rec in token_id:
            if rec.estimated_date and rec.estimated_date > fields.Datetime.now():
                rec.unlink()

