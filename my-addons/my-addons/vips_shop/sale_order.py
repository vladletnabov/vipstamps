# -*- coding: utf-8 -*-
#from openerp import fields, models, osv
import random

from openerp import SUPERUSER_ID
import openerp.addons.decimal_precision as dp
from openerp.osv import osv, orm, fields
from openerp.addons.web.http import request
from openerp.tools.translate import _

import logging
#Get the logger
_logger = logging.getLogger(__name__)


class sale_order(osv.osv):
    #_name = "sale.order"
    _inherit = 'sale.order'

    # id_session (ID сессии если заказа через ИМ)
    # id_delivery (ID места доставки ели доставка по адресу клиента или самовывоз из филиала)
    # id_metrostation (ID станции метро доставки)
    # type_delivery (Тип доставки)
    # price_delivery (Стоимость доставки)
    # courier (ID курьера)


    _columns = {
    #'shipaddr' : fields.many2many('res.partner', string="Shipping address", readonly=False),

    #'shipaddr' : fields.many2many('res.partner', 'vips_shop_order_to_ship_rel', 'shipaddr', 'partner_id', string="Shipping address"),
    'shipaddr' : fields.many2one('res.partner',string="Shipping address"),
    'metro'    : fields.many2one('vips_shop.metro', string="Metro stations"),
    'typeship' : fields.many2one('vips_shop.delivery',  string="Type delivery", readonly=False),
    # priceship= через typeship привязка к продукту
    #'courier'  : fields.many2many('res.partner', 'vips_shop_courier_for_ship_rel', 'sale_order_id', 'partner_id',string="Shipping courier", readonly=False),
    'courier'  : fields.many2one('res.partner', string="Shipping courier", readonly=False),
    #'usersess' : fields.one2many('vips_vc.session', 'order_id', string="Session customer", readonly=False),
    'usersess' : fields.many2one('vips_vc.session', string="Session customer", readonly=False),
    'quick_order_id' : fields.one2many('vips_shop.quick_sale_order', 'order_id', string="Быстрый заказ", readonly=False),
    }

class website(orm.Model):
    _inherit = 'website'

    def sale_get_order(self, cr, uid, ids, force_create=False, code=None, update_pricelist=None, context=None):
        sale_order_obj = self.pool['sale.order']
        sale_order_id = request.session.get('sale_order_id')
        sale_order = None
        webcalc_session_id = request.session['webcalc_session_id']

        # Test validity of the sale_order_id
        if sale_order_id and sale_order_obj.exists(cr, SUPERUSER_ID, sale_order_id, context=context):
            sale_order = sale_order_obj.browse(cr, SUPERUSER_ID, sale_order_id, context=context)
        else:
            sale_order_id = None

        # create so if needed
        if not sale_order_id and (force_create or code):
            # TODO cache partner_id session
            partner = self.pool['res.users'].browse(cr, SUPERUSER_ID, uid, context=context).partner_id

            for w in self.browse(cr, uid, ids):
                values = {
                    'user_id': w.user_id.id,
                    'partner_id': partner.id,
                    'pricelist_id': partner.property_product_pricelist.id,
                    'section_id': self.pool.get('ir.model.data').get_object_reference(cr, uid, 'website', 'salesteam_website_sales')[1],
                }

                #if (webcalc_session_id != None):
                #    values['usersess'] = webcalc_session_id
                _logger.error(">>>>>   %r", values)
                sale_order_id = sale_order_obj.create(cr, SUPERUSER_ID, values, context=context)
                values = sale_order_obj.onchange_partner_id(cr, SUPERUSER_ID, [], partner.id, context=context)['value']
                sale_order_obj.write(cr, SUPERUSER_ID, [sale_order_id], values, context=context)
                sale_order_obj.write(cr, SUPERUSER_ID, [sale_order_id], {'usersess': webcalc_session_id }, context=context)
                request.session['sale_order_id'] = sale_order_id
                sale_order = sale_order_obj.browse(cr, SUPERUSER_ID, sale_order_id, context=context)

        if sale_order_id:
            # TODO cache partner_id session
            partner = self.pool['res.users'].browse(cr, SUPERUSER_ID, uid, context=context).partner_id
            # check for change of pricelist with a coupon
            if code and code != sale_order.pricelist_id.code:
                pricelist_ids = self.pool['product.pricelist'].search(cr, SUPERUSER_ID, [('code', '=', code)], context=context)
                if pricelist_ids:
                    pricelist_id = pricelist_ids[0]
                    request.session['sale_order_code_pricelist_id'] = pricelist_id
                    update_pricelist = True

            pricelist_id = request.session.get('sale_order_code_pricelist_id') or partner.property_product_pricelist.id

            # check for change of partner_id ie after signup
            if sale_order.partner_id.id != partner.id and request.website.partner_id.id != partner.id:
                flag_pricelist = False
                if pricelist_id != sale_order.pricelist_id.id:
                    flag_pricelist = True
                fiscal_position = sale_order.fiscal_position and sale_order.fiscal_position.id or False

                values = sale_order_obj.onchange_partner_id(cr, SUPERUSER_ID, [sale_order_id], partner.id, context=context)['value']
                if values.get('fiscal_position'):
                    order_lines = map(int,sale_order.order_line)
                    values.update(sale_order_obj.onchange_fiscal_position(cr, SUPERUSER_ID, [],
                        values['fiscal_position'], [[6, 0, order_lines]], context=context)['value'])

                values['partner_id'] = partner.id
                sale_order_obj.write(cr, SUPERUSER_ID, [sale_order_id], values, context=context)

                if flag_pricelist or values.get('fiscal_position', False) != fiscal_position:
                    update_pricelist = True

            # update the pricelist
            if update_pricelist:
                values = {'pricelist_id': pricelist_id}
                values.update(sale_order.onchange_pricelist_id(pricelist_id, None)['value'])
                sale_order.write(values)
                for line in sale_order.order_line:
                    if line.exists():
                        sale_order._cart_update(product_id=line.product_id.id, line_id=line.id, add_qty=0)

            # update browse record
            if (code and code != sale_order.pricelist_id.code) or sale_order.partner_id.id !=  partner.id:
                sale_order = sale_order_obj.browse(cr, SUPERUSER_ID, sale_order.id, context=context)

        else:
            request.session['sale_order_id'] = None
            return None

        return sale_order