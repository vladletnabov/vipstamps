# -*- coding: utf-8 -*-
from openerp import fields, models

class user(models.Model):
    _inherit = 'res.users'

    salepersone_id= fields.One2many('vips_shop.salepersone','name', string="Default salepersone for order", readonly=False)
