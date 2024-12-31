from odoo import models, api
from odoo import fields
from odoo.exceptions import ValidationError


class Property(models.Model):
    _name = 'property'
    _description = 'Property'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True, size=20)
    ref = fields.Char(default='New', readonly=True)
    description = fields.Char(tracking=1)
    postcode = fields.Char(required=True)
    date_availability = fields.Date(tracking=1)
    expected_selling_date = fields.Date(tracking=1)
    is_late = fields.Boolean()
    expected_price = fields.Float()
    selling_price = fields.Float()
    diff = fields.Float(compute='_compute_diff')
    bed_rooms = fields.Integer(required=True)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    active = fields.Boolean(default=True)
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ], default='north')

    owner_id = fields.Many2one('owner')
    tag_ids = fields.Many2many('tag')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
        ('closed', 'Closed'),
    ], default='draft')

    owner_address = fields.Char(related='owner_id.address')
    owner_phone = fields.Char(related='owner_id.phone')
    create_time = fields.Datetime(default=fields.Datetime.now())

    _sql_constraints = [
        ('unique_name', 'unique("name")', 'This name is exist!')
    ]

    line_ids = fields.One2many('property.line', 'property_id')

    def property_xlsx_report(self):
        return {
            'type':'ir.actions.act_url',
            'url':f'/property/excel/report/{self.env.context.get("active_ids")}',
            'target':'new'
        }

    def check_expected_selling_date(self):
        property_ids = self.search([])
        for rec in property_ids:
            if rec.expected_selling_date and rec.expected_selling_date < fields.date.today():
                rec.is_late = True

        # for rec in property_ids:
        #     if rec.state == 'sold':
        #         rec.is_late = False

    @api.depends('expected_price', 'selling_price', 'owner_id.phone')
    def _compute_diff(self):
        for rec in self:
            rec.diff = rec.selling_price - rec.expected_price

    # @api.onchange('expected_price', 'owner_id.phone')
    # def _onchange_expected_price(self):
    #     for rec in self:
    #         print(rec)
    #         print("inside _onchange_expected_price method")

    def action_draft(self):
        for rec in self:
            rec.create_history_record(rec.state, 'draft')
            rec.state = 'draft'
            # rec.write({
            #     'state': 'draft'
            # })

    def action_pending(self):
        for rec in self:
            rec.create_history_record(rec.state, 'pending')
            rec.state = 'pending'

    def action_sold(self):
        for rec in self:
            rec.create_history_record(rec.state, 'sold')
            rec.state = 'sold'

    def action_closed(self):
        for rec in self:
            rec.create_history_record(rec.state, 'closed')
            rec.state = 'closed'

    def action(self):
        print(self.env['owner'].search([]))

    def action_1(self):
        print(self.env['owner'].create({
            'name': 'name four',
            'phone': '01000050'
        }))

    @api.constrains('bed_rooms')
    def _check_bedrooms_greater_zero(self):
        for rec in self:
            if rec.bed_rooms == 0:
                raise ValidationError('please add a valid value for bedrooms')

        #Crud_Opertations
    @api.model
    def create(self, vals):
        res = super(Property, self).create(vals)
        if res.ref=='new':
            res.ref=res.env['ir.sequence'].next_by_code('property_seq')
        return res
    
    # @api.model
    # def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
    #     res = super(Property, self)._search(domain, offset=0, limit=None, order=None, access_rights_uid=None)
    #     print('inside search method')
    #     return res
    #
    # def write(self, vals):
    #     res = super(Property, self).write(vals)
    #     print('inside write method')
    #     return res
    #
    # def unlink(self):
    #     res = super(Property, self).unlink()
    #     print('inside delete method')
    #     return res

    def create_history_record(self, old_state, new_state, reason=""):
        for rec in self:
            rec.env['property.history'].create({
                'user_id': rec.env.uid,
                'property_id': rec.env.uid,
                'old_state': old_state,
                'new_state': new_state,
                'reason': reason or "",
                'line_ids': [(0, 0, {'description': line.description, 'area': line.area}) for line in rec.line_ids],
                })


    def action_open_change_state_wizard(self):
        action = self.env['ir.actions.actions']._for_xml_id('app_one.change_state_wizard_action')
        action['context'] = {'default_property_id': self.id}
        return action

class PropertyLine(models.Model):
    _name = 'property.line'

    property_id = fields.Many2one('property')
    area = fields.Float()
    description = fields.Char()