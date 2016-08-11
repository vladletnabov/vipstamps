# -*- coding: utf-8 -*-

from openerp import models, fields, api

#from openerp.osv import osv, orm
from openerp import SUPERUSER_ID


# class vips_shop(models.Model):
#     _name = 'vips_shop.vips_shop'

#     name = fields.Char()
class metro(models.Model):
    _name = 'vips_shop.metro'
    name = fields.Char()
    #colorLine = fields.Char()
    color_ids = fields.Many2one('vips_shop.color',
                                            string='Metro line color', index=True)
    partners_ids = fields.Many2many('res.partner', string="Contacts")
    delivery_id = fields.Many2many('vips_shop.delivery',  string="Delivery")
    order_id = fields.One2many('sale.order', 'metro', string="Order")


class color(models.Model):
    _name = 'vips_shop.color'
    name = fields.Char()
    number = fields.Integer()
    color = fields.Char()
    metro_id = fields.One2many('vips_shop.metro', 'color_ids',
                                            string='Metro station', index=True)


class delivery(models.Model):
    _name = 'vips_shop.delivery'
    name = fields.Char()
    prefix_address = fields.Char()
    product_id = fields.Many2one('product.template',  string='Metro line color', index=True)
    metro_ids = fields.Many2many('vips_shop.metro',  string='Metro Station', index=True)
    filial_ids = fields.Many2many('res.partner',  string='Filials', index=True)
    order_id = fields.One2many('sale.order', 'typeship', string="Order", readonly=False)

class filial(models.Model):
    _name = 'vips_shop.filial'
    name = fields.Many2one('res.partner',  string='Filials', index=True)
    type = fields.Selection([('office', 'Офис продаж'),('point','Точка выдачи заказа')])

class quick_price(models.Model):
    _name = 'vips_shop.quick_price'

    name = fields.Char(required="True")
    product_id = fields.Many2one('product.template',  string='Связанный продукт', required="True", index=True)

class quick_sale_order(models.Model):
    _name = 'vips_shop.quick_sale_order'

    name = fields.Char()
    order_id = fields.Many2one('sale.order', string="Связанный заказ", readonly=False)
    partner_id = fields.Many2one('res.partner', string="Информация о заказчике")
    description = fields.Text(string="Информация о заказе")

    def get_quick_name(self):
        name = "БЗ-" + str(self.id)
        return name


class website(models.Model):
    _inherit = 'website'

    def get_filials(self,cr, uid, ids, context=None):
        #orm_filial =  self.pool(['vips_shop.filial'])
        #result= []
        orm_filial = self.pool.get('vips_shop.filial')

        filial_ids = orm_filial.search(cr, SUPERUSER_ID, [], context=context)
        filials = orm_filial.browse(cr, SUPERUSER_ID, filial_ids, context)

        #filial_ids = orm_filial.search(cr, SUPERUSER_ID, [], context=context)
        #filials = orm_filial.browse(cr, SUPERUSER_ID, filial_ids, context)[0]

        #for (i, filial) in enumerate(filials):
        #    result[i] = filial

        return filials

    def get_quick_product(self,cr, uid, ids, context=None):
        orm_quick_product = self.pool.get('vips_shop.quick_price')

        product_ids = orm_quick_product.search(cr, SUPERUSER_ID, [], context=context)
        products = orm_quick_product.browse(cr, SUPERUSER_ID, product_ids, context)
        return products

    def get_vips_delivery(self,cr, uid, ids, context=None):
        orm_quick_product = self.pool.get('vips_shop.delivery')

        delivery_ids = orm_quick_product.search(cr, SUPERUSER_ID, [], context=context)
        deliveris = orm_quick_product.browse(cr, SUPERUSER_ID, delivery_ids, context)
        return deliveris
