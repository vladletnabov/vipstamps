# -*- coding: utf-8 -*-
from openerp import fields, models

class Partner(models.Model):
    _inherit = 'res.partner'

    # Add a new column to the res.partner model, by default partners are not
    # instructors
    #instructor = fields.Boolean("Instructor", default=False)
    #
    #session_ids = fields.Many2many('openacademy.session',
    #    string="Attended Sessions", readonly=True)

    station_ids = fields.Many2many('vips_shop.metro', string="Metro stations", readonly=False)
    delivey_ids = fields.Many2many('vips_shop.delivery', 'filial_ids', string="Delivery")

    #order_addr  = fields.Many2many('sale.order','vips_shop_order_to_ship_rel', 'partner_id', 'sale_order_id', string="Order for address", readonly=False)
    #order_cour  = fields.Many2many('sale.order', 'vips_shop_courier_for_ship_rel', 'partner_id', 'sale_order_id', string="Order for Courier", readonly=False)

    order_addr    = fields.One2many('sale.order','shipaddr', string="Order for address", readonly=False)
    order_cour    = fields.One2many('sale.order','shipaddr', string="Order for address", readonly=False)
    #filial_lst  = fields.One2many('vips_shop.filial', 'partner_id', string="Filial", readonly=False)
    #quickordr   = fields.One2many('vips_shop.quick_sale_order',  'partner_id', string="Быстрый заказ")
