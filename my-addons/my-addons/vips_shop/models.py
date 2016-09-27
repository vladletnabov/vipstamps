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

class salepersone(models.Model):
    _name = 'vips_shop.salepersone'

    name = fields.Many2one('res.users',  string='salepersone', index=True)

#    fp_product  -filial page products
class fp_product (models.Model):
    _name = 'vips_shop.fp_product'

    name = fields.Char()
    active = fields.Boolean()
    rstamp_ids = fields.Many2one('vips_shop.fp_product_group',  string='Печати', index=True)
    sqstamp_man_ids = fields.Many2one('vips_shop.fp_product_group',  string='Штампы на ручке', index=True)
    sqstamp_auto_ids = fields.Many2one('vips_shop.fp_product_group',  string='Штампы на автомате', index=True)
    faximile_ids = fields.Many2one('vips_shop.fp_product_group',  string='Факсимиле', index=True)

class fp_product_param(models.Model):
    _name = 'vips_shop.fp_product_param'
    name = fields.Char()
    cushion = fields.Selection([('no', 'нет'),('yes','встроена')])
    equipment = fields.Selection([('manual', 'ручная'),('auto','автоматическая'),('mobile','карманная')])
    product_id = fields.Many2one('product.template',  string='Связанный продукт', index=True)
    '''rstamp_ids = fields.One2many('vips_shop.fp_product', 'rstamp_ids', string='Печати', index=True)
    sqstamp_man_ids = fields.One2many('vips_shop.fp_product', 'sqstamp_man_ids',  string='Штампы на ручке', index=True)
    sqstamp_auto_ids = fields.One2many('vips_shop.fp_product', 'sqstamp_auto_ids',  string='Штампы на автомате', index=True)
    faximile_ids = fields.One2many('vips_shop.fp_product', 'faximile_ids',  string='Факсимиле', index=True)'''
    fp_product_group_id = fields.Many2many('vips_shop.fp_product_group', 'vips_product_param_w_group_rel', 'fp_product_param_id', 'fp_product_group_id',  string='Группа к которй привязан продукт', index=True)

class fp_product_group(models.Model):
    _name = 'vips_shop.fp_product_group'
    name = fields.Char()
    fp_product_param_id = fields.Many2many('vips_shop.fp_product_param',  'vips_product_param_w_group_rel', 'fp_product_group_id', 'fp_product_param_id',string='Связанные продукты группы', index=True)
    rstamp_ids = fields.One2many('vips_shop.fp_product', 'rstamp_ids', string='Печати', index=True)
    sqstamp_man_ids = fields.One2many('vips_shop.fp_product', 'sqstamp_man_ids',  string='Штампы на ручке', index=True)
    sqstamp_auto_ids = fields.One2many('vips_shop.fp_product', 'sqstamp_auto_ids',  string='Штампы на автомате', index=True)
    faximile_ids = fields.One2many('vips_shop.fp_product', 'faximile_ids',  string='Факсимиле', index=True)

class filial_page(models.Model):
    _name = 'vips_shop.filial_page'
    name = fields.Char()
    predlog = fields.Char()
    padej = fields.Char()
    url_name = fields.Char(required=True)
    #filial_id = fields.Many2one()
    header_text = fields.Char()
    sub_header_text = fields.Char()
    lvl3_header_text = fields.Char()
    main_text = fields.Html()
    banner_id = fields.Many2one('vips_shop.filial_banner',  string='Баннер', index=True)

    _sql_constraints = [
        ('url_name', 'unique(url_name)', 'Данное пое должно быть уникальным!'),
    ]




class filial_banner(models.Model):
    _name = 'vips_shop.filial_banner'

    name = fields.Char()
    filial_page_ids = fields.One2many('vips_shop.filial_page', 'banner_id',  string='Штампы на автомате', index=True)
    banner_item_ids = fields.Many2many('vips_shop.banner_item',  'vips_banner_item_rel', 'banner_item_ids', 'filail_baner_ids',string='Связанные банер', index=True)

class banner_item(models.Model):
    _name = 'vips_shop.banner_item'

    name = fields.Char()
    text = fields.Char()
    image = fields.Binary()
    filail_baner_ids = fields.Many2many('vips_shop.filial_banner',  'vips_banner_item_rel', 'banner_item_ids', 'filail_baner_ids',string='Связанные банер', index=True)





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

    def get_all_filial_pages(self,cr, uid, ids, context=None):
        orm_fp = self.pool.get('vips_shop.filial_page')
        fp_ids = orm_fp.search(cr, SUPERUSER_ID, [], context=context)
        count_pages = len(orm_fp.browse(cr, SUPERUSER_ID, fp_ids, context))
        if count_pages==0:
            #page = 'website.page_404'
            #return request.render(page, {'path': url,})
            return []

        pages = orm_fp.browse(cr, SUPERUSER_ID, fp_ids, context)
        return pages
