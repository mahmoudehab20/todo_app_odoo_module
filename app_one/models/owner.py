from odoo import models
from odoo import fields


class Owner(models.Model):
    _name = 'owner'

    name = fields.Char(required=True, size=50)
    phone = fields.Char(required=True, size=12)
    address = fields.Char()
    property_ids = fields.One2many('property', 'owner_id')

