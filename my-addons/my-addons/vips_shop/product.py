# -*- coding: utf-8 -*-
from openerp import fields, models

class product(models.Model):
    _inherit = 'product.template'

    # Add a new column to the res.partner model, by default partners are not
    # instructors
    #instructor = fields.Boolean("Instructor", default=False)
    #
    #session_ids = fields.Many2many('openacademy.session',
    #    string="Attended Sessions", readonly=True)

    station_ids = fields.Many2many('vips_shop.metro', string="Metro stations", readonly=False)
    delivery_ids = fields.One2many('vips_shop.delivery', 'product_id', string="Delivery to")
    quick_price_ids = fields.One2many('vips_shop.quick_price', 'product_id', string="Quick price product")

