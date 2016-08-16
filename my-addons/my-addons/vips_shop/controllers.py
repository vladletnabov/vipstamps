# -*- coding: utf-8 -*-
from openerp import http
from openerp.addons.website_sale.controllers.main import website_sale
import logging
import werkzeug

from openerp import SUPERUSER_ID
from openerp.http import request
from openerp.tools.translate import _
from openerp.addons.website.models.website import slug
from openerp.addons.web.controllers.main import login_redirect
#Import logger
import logging
#Get the logger
_logger = logging.getLogger(__name__)


class vip_stamp_web_shop(website_sale):

    @http.route()
    def checkout(self, **post):
        cr, uid, context = request.cr, request.uid, request.context

        order = request.website.sale_get_order(force_create=1, context=context)

        redirection = self.checkout_redirection(order)
        if redirection:
            return redirection

        values = self.checkout_values()

        return request.website.render("vips_shop.checkout", values)

    @http.route(['/vips_shop/filial_list'],type='json', auth="public", website=True)
    def filial_list(self,**post):
        cr, uid, context, registry = request.cr, request.uid, request.context, request.registry
        orm_partner = registry.get('res.partner')
        #orm_metro = registry.get('vips_shop.metro')
        #orm_delivery = registry.get('vips_shop.delivery')
        orm_filial = registry.get('vips_shop.filial')
        values = {}

        filial_ids = orm_filial.search(cr, SUPERUSER_ID, [], context=context)
        filials = orm_filial.browse(cr, SUPERUSER_ID, filial_ids, context)
        main_office = orm_partner.browse(cr, SUPERUSER_ID, 1, context)

        if len(filials)>0:
            # without indexes
            for filial in filials:
                #print filial
                filial_data = {
                    'name': filial.name.name,
                    'address': filial.name.street2,
                    'workday_from':'Пн',
                    'workday_from':'Пт',
                    'workday_time_from':'09:00',
                    'workday_time_to':'19:00',
                    'weekend_from':'Сб',
                    'weekend_from':'Вс',
                    'weekend_time_from':'',
                    'weekend_time_to':'',
                    'weekend_str': 'по согласованию'
                }
                values['filial.name.name,'] = filial_data
            values['phone'] = main_office.phone
        else:
            values = {
                'error': 'error'
            }


        return values

    def checkout_values(self, data=None):
        _logger.error('checkout_values() ')
        cr, uid, context, registry = request.cr, request.uid, request.context, request.registry
        orm_partner = registry.get('res.partner')
        orm_user = registry.get('res.users')
        orm_country = registry.get('res.country')
        state_orm = registry.get('res.country.state')
        orm_metro = registry.get('vips_shop.metro')
        orm_delivery = registry.get('vips_shop.delivery')

        country_ids = orm_country.search(cr, SUPERUSER_ID, [], context=context)
        countries = orm_country.browse(cr, SUPERUSER_ID, country_ids, context)
        states_ids = state_orm.search(cr, SUPERUSER_ID, [], context=context)
        states = state_orm.browse(cr, SUPERUSER_ID, states_ids, context)
        partner = orm_user.browse(cr, SUPERUSER_ID, request.uid, context).partner_id
        metro_stations_ids = orm_metro.search(cr, SUPERUSER_ID, [], context=context)
        metro_stations = orm_metro.browse(cr, SUPERUSER_ID, metro_stations_ids, context)
        #delivery_ids = orm_delivery.search(cr, SUPERUSER_ID, ['name', '=', 'metro'], context=context)
        #delivery_metro = orm_delivery.browse(cr, SUPERUSER_ID, delivery_ids, context)
        #delivery_ids = None
        delivery_filial_ids = orm_delivery.search(cr, SUPERUSER_ID, [['name', '=', 'filial'],], context=context)
        delivery_filail = orm_delivery.browse(cr, SUPERUSER_ID, delivery_filial_ids, context)
        delivery_filial_product = delivery_filail.product_id

        #delivery_filial_product_id = delivery_filial_product.id
        #delivery_filial_price = delivery_filial_product.list_price
        #delivery_filial_price = [str(delivery_filial_product.id), str(delivery_filial_product.list_price)]


        delivery_metro_ids = orm_delivery.search(cr, SUPERUSER_ID, [['name', '=', 'metro'],], context=context)
        delivery_metro = orm_delivery.browse(cr, SUPERUSER_ID, delivery_metro_ids, context)
        delivery_metro_product = delivery_metro.product_id
        #delivery_metro_price = [str(delivery_metro_product.id), str(delivery_metro_product.list_price)]

        delivery_address_ids = orm_delivery.search(cr, SUPERUSER_ID, [['name', '=', 'address'],], context=context)
        delivery_address = orm_delivery.browse(cr, SUPERUSER_ID, delivery_address_ids, context)
        delivery_address_product = delivery_address.product_id


        for val in metro_stations:
            _logger.error("metro_stations: %r",val)

        station_id= None

        if (partner.station_ids!=None):
            station_id = partner.station_ids.id

        order = None

        shipping_id = None
        shipping_ids = []
        checkout = {}
        if not data:
            if request.uid != request.website.user_id.id:
                checkout.update( self.checkout_parse("billing", partner) )
                shipping_ids = orm_partner.search(cr, SUPERUSER_ID, [("parent_id", "=", partner.id), ('type', "=", 'delivery')], context=context)
            else:
                order = request.website.sale_get_order(force_create=1, context=context)
                if order.partner_id:
                    domain = [("partner_id", "=", order.partner_id.id)]
                    user_ids = request.registry['res.users'].search(cr, SUPERUSER_ID, domain, context=dict(context or {}, active_test=False))
                    if not user_ids or request.website.user_id.id not in user_ids:
                        checkout.update( self.checkout_parse("billing", order.partner_id) )
        else:
            checkout = self.checkout_parse('billing', data)
            try:
                shipping_id = int(data["shipping_id"])
            except ValueError:
                pass
            if shipping_id == -1:
                checkout.update(self.checkout_parse('shipping', data))

        #shiping_office = orm_partner.search(cr, uid, [('type', "=", 'contact')], context=context)
        #shiping_office = orm_partner.browse(1)
        #_logger.error('SHIPPING_OFFICE : %r', shiping_office)

        if shipping_id is None:
            if not order:
                order = request.website.sale_get_order(context=context)
            if order and order.partner_shipping_id:
                shipping_id = order.partner_shipping_id.id

        shipping_ids = list(set(shipping_ids) - set([partner.id]))
        _logger.error('shipping_ids before : %r', shipping_ids)
        '''shipping_ids.append(1)
        for office in shiping_office:
            if shipping_id != office:
                _logger.error('add office to shiping_ids  : %r', office)
                shipping_ids.append(office)
            else:
                _logger.error('shipping_id == office! %r == %r', shipping_id, office)'''
        _logger.error('shipping_ids after : %r', shipping_ids)

        if shipping_id == partner.id:
            shipping_id = 0
        elif shipping_id > 0 and shipping_id not in shipping_ids:
            shipping_ids.append(shipping_id)
        elif shipping_id is None and shipping_ids:
            shipping_id = shipping_ids[0]

        ctx = dict(context, show_address=1)
        shippings = []
        if shipping_ids:
            shippings = shipping_ids and orm_partner.browse(cr, SUPERUSER_ID, list(shipping_ids), ctx) or []
        if shipping_id > 0:
            shipping = orm_partner.browse(cr, SUPERUSER_ID, shipping_id, ctx)
            checkout.update( self.checkout_parse("shipping", shipping) )

        checkout['shipping_id'] = shipping_id

        # Default search by user country
        if not checkout.get('country_id'):
            country_code = request.session['geoip'].get('country_code')
            if country_code:
                country_ids = request.registry.get('res.country').search(cr, uid, [('code', '=', country_code)], context=context)
                if country_ids:
                    checkout['country_id'] = country_ids[0]

        values = {
            'countries': countries,
            'states': states,
            'checkout': checkout,
            'shipping_id': partner.id != shipping_id and shipping_id or 0,
            'shippings': shippings,
            'error': {},
            'metro_stations': metro_stations,
            'station_id': station_id,
            #'delivery_metro': delivery_metro,
            'delivery_address_product': delivery_address_product,
            'delivery_metro_product': delivery_metro_product,
            'delivery_filial_product': delivery_filial_product,
            'delivery_filail': delivery_filail,
            'has_check_vat': hasattr(registry['res.partner'], 'check_vat')
        }

        return values

    @http.route()
    def confirm_order(self, **post):
        cr, uid, context, registry = request.cr, request.uid, request.context, request.registry

        order = request.website.sale_get_order(context=context)
        if not order:
            return request.redirect("/shop")

        redirection = self.checkout_redirection(order)
        if redirection:
            return redirection

        values = self.checkout_values(post)
        _logger.error('confirm_order values : %r', values.keys())
        values["error"] = self.checkout_form_validate(values["checkout"])
        if values["error"]:
            return request.website.render("vips_shop.checkout", values)

        self.checkout_form_save(values["checkout"])

        request.session['sale_last_order_id'] = order.id

        request.website.sale_get_order(update_pricelist=True, context=context)

        #записываем информацию о доставке
        _logger.error("----! post: %r", post)
        self.write_shipping_info(post)

        return request.redirect("/shop/payment")

    def checkout_form_validate(self, data):
        cr, uid, context, registry = request.cr, request.uid, request.context, request.registry

        # Validation
        error = dict()
        for field_name in self._get_mandatory_billing_fields():
            if not data.get(field_name):
                error[field_name] = 'missing'

        if data.get("vat") and hasattr(registry["res.partner"], "check_vat"):
            if request.website.company_id.vat_check_vies:
                # force full VIES online check
                check_func = registry["res.partner"].vies_vat_check
            else:
                # quick and partial off-line checksum validation
                check_func = registry["res.partner"].simple_vat_check
            vat_country, vat_number = registry["res.partner"]._split_vat(data.get("vat"))
            if not check_func(cr, uid, vat_country, vat_number, context=None): # simple_vat_check
                error["vat"] = 'error'

        if data.get("shipping_id") == -1:
            for field_name in self._get_mandatory_shipping_fields():
                field_name = 'shipping_' + field_name
                if not data.get(field_name):
                    error[field_name] = 'missing'

        return error

    def checkout_form_save(self, checkout):
        cr, uid, context, registry = request.cr, request.uid, request.context, request.registry

        order = request.website.sale_get_order(force_create=1, context=context)

        orm_partner = registry.get('res.partner')
        orm_user = registry.get('res.users')
        order_obj = request.registry.get('sale.order')

        partner_lang = request.lang if request.lang in [lang.code for lang in request.website.language_ids] else None

        billing_info = {'customer': True}
        if partner_lang:
            billing_info['lang'] = partner_lang
        billing_info.update(self.checkout_parse('billing', checkout, True))

        # set partner_id
        partner_id = None
        if request.uid != request.website.user_id.id:
            partner_id = orm_user.browse(cr, SUPERUSER_ID, uid, context=context).partner_id.id
        elif order.partner_id:
            user_ids = request.registry['res.users'].search(cr, SUPERUSER_ID,
                [("partner_id", "=", order.partner_id.id)], context=dict(context or {}, active_test=False))
            if not user_ids or request.website.user_id.id not in user_ids:
                partner_id = order.partner_id.id

        # save partner informations
        if partner_id and request.website.partner_id.id != partner_id:
            orm_partner.write(cr, SUPERUSER_ID, [partner_id], billing_info, context=context)
        else:
            # create partner
            partner_id = orm_partner.create(cr, SUPERUSER_ID, billing_info, context=context)

        # create a new shipping partner
        if checkout.get('shipping_id') == -1:
            shipping_info = self._get_shipping_info(checkout)
            if partner_lang:
                shipping_info['lang'] = partner_lang
            shipping_info['parent_id'] = partner_id
            checkout['shipping_id'] = orm_partner.create(cr, SUPERUSER_ID, shipping_info, context)
            _logger.info("<---> shipping_info: %r", shipping_info)

        _logger.info("|---> partner_id: %r", partner_id)

        order_info = {
            'partner_id': partner_id,
            'message_follower_ids': [(4, partner_id), (3, request.website.partner_id.id)],
            'partner_invoice_id': partner_id,
        }
        _logger.info("|---> order_info: %r", order_info)
        order_info.update(order_obj.onchange_partner_id(cr, SUPERUSER_ID, [], partner_id, context=context)['value'])
        _logger.error("||--> CHECKING checkout.get('shipping_id')!=-2 : %r", checkout.get('shipping_id'))
        if (checkout.get('shipping_id')!=-2):
            address_change = order_obj.onchange_delivery_id(cr, SUPERUSER_ID, [], order.company_id.id, partner_id,
                                                        checkout.get('shipping_id'), None, context=context)['value']
            order_info.update(address_change)
            if address_change.get('fiscal_position'):
                fiscal_update = order_obj.onchange_fiscal_position(cr, SUPERUSER_ID, [], address_change['fiscal_position'],
                                                               [(4, l.id) for l in order.order_line], context=None)['value']
                order_info.update(fiscal_update)

        order_info.pop('user_id')
        if (checkout.get('shipping_id')==-2):
            order_info.update(partner_shipping_id=0 or partner_id)
        else:
            order_info.update(partner_shipping_id=checkout.get('shipping_id') or partner_id)

        order_obj.write(cr, SUPERUSER_ID, [order.id], order_info, context=context)


    def write_shipping_info(self, *post):
        cr, uid, context, registry = request.cr, request.uid, request.context, request.registry
        orm_orderline = request.env['sale.order.line']
        orm_delivery = request.env['vips_shop.delivery']
        add_qty=1
        set_qty=0
        line_ids={}

        order = request.website.sale_get_order()
        if order.state != 'draft':
            request.website.sale_reset()
            return {}

        # Сначала нужно удалить все записи о доставке
        # для этого ищем в sale_order_line для order_id product_id и получаем line_id
        # всё это загоняем в общий словарь line_ids [product_id] = line_id
        deliveries = orm_delivery.sudo().search([])
        for (i, delivery) in enumerate(deliveries):
            #print i, item
            orderline_id = orm_orderline.sudo().search([['product_id','=',delivery.product_id.id],
                                                        ['order_id', '=', order.id]])
            if orderline_id:
                line_ids[delivery.product_id.id] = orderline_id

        for product_id in line_ids:
            _logger.error("order._cart_update(product_id=%r, line_id=%r, add_qty=0, set_qty=0)", product_id, line_ids[product_id].id )
            value = order._cart_update(product_id=product_id, line_id=line_ids[product_id].id, add_qty=None, set_qty=None)

        _logger.error("---!! post: %r", post)
        shipping_id = int(post[0]['shipping_id'])
        shipping_product_id = int(post[0]['shipping_product_id'])
        shipping_product_id = orm_delivery.sudo().search([('product_id','=',shipping_product_id)])
        shipping = orm_delivery.browse(shipping_product_id)[0].id
        _logger.error("---|| shipping: %s", shipping)
        #shipping_name = shipping.name
        _logger.error("---!! shipping_id: %r", shipping_id)
        shipping_value={
            'shipaddr':None,
            'metro':[],
            'typeship': shipping_product_id.id
        }
        if(shipping_id==-2):
            _logger.info("shipping to metro post[0] : ", post[0])
            metro_id = int(post[0]['shipping_to_metro_id'])
            shipping_value={
                'shipaddr':None,
                'metro':metro_id ,
                'typeship': shipping_product_id.id
            }
        elif(shipping_id==-1):
            _logger.info('shipping to secondary address')
            shipping_value={
                'shipaddr':order.partner_shipping_id.id,
                'metro':None ,
                'typeship': shipping_product_id.id
            }
        elif(shipping_id==0):
            _logger.info('shipping to primary address')
            shipping_value={
                'shipaddr':order.partner_id.id,
                'metro':[]  ,
                'typeship': shipping_product_id.id
            }
        else:
            _logger.info('any shipping...')
            #if(shipping_name=='filial'):
            _logger.info('shipping to filial...')
            shipping_value={
                'shipaddr':shipping_id,
                'metro':None,
                'typeship': shipping_product_id.id
            }
            #else:
            #    _logger.info('shipping to another address')

        #shipping_value['typeship'] = shipping_product_id
        _logger.error("---!! shipping_value: %r", shipping_value)
        order.write(shipping_value)
        _logger.error("---!! shipping.product_id.id: %r", shipping.product_id)
        order._cart_update(product_id=int(shipping.product_id.id), add_qty=float(add_qty), set_qty=float(set_qty))
        order.env.cr.commit()

        # образец удаления/добавления в заказ позиций
        #value = order._cart_update(product_id=product_id, line_id=line_id, add_qty=add_qty, set_qty=set_qty)

        # удаление заказа если стоимость равна нулю
        #if not order.cart_quantity:
        #    request.website.sale_reset()
        #    return {}



        return None


    @http.route()
    def payment(self, **post):
        """ Payment step. This page proposes several payment means based on available
        payment.acquirer. State at this point :

         - a draft sale order with lines; otherwise, clean context / session and
           back to the shop
         - no transaction in context / session, or only a draft one, if the customer
           did go to a payment.acquirer website but closed the tab without
           paying / canceling
        """
        cr, uid, context = request.cr, request.uid, request.context
        payment_obj = request.registry.get('payment.acquirer')
        sale_order_obj = request.registry.get('sale.order')

        order = request.website.sale_get_order(context=context)
        order.write({'usersess': request.session['webcalc_session_id']})
        #order.env.cr.commit()
        redirection = self.checkout_redirection(order)
        if redirection:
            return redirection

        shipping_partner_id = False
        if order:
            if order.partner_shipping_id.id:
                shipping_partner_id = order.partner_shipping_id.id
            else:
                shipping_partner_id = order.partner_invoice_id.id

        values = {
            'order': request.registry['sale.order'].browse(cr, SUPERUSER_ID, order.id, context=context),
            'usersess': request.session['webcalc_session_id']
        }
        values['errors'] = sale_order_obj._get_errors(cr, uid, order, context=context)
        values.update(sale_order_obj._get_website_data(cr, uid, order, context))

        if not values['errors']:
            acquirer_ids = payment_obj.search(cr, SUPERUSER_ID, [('website_published', '=', True), ('company_id', '=', order.company_id.id)], context=context)
            values['acquirers'] = list(payment_obj.browse(cr, uid, acquirer_ids, context=context))
            render_ctx = dict(context, submit_class='btn btn-primary', submit_txt=_('Pay Now'))
            for acquirer in values['acquirers']:
                acquirer.button = payment_obj.render(
                    cr, SUPERUSER_ID, acquirer.id,
                    '/',
                    order.amount_total,
                    order.pricelist_id.currency_id.id,
                    partner_id=shipping_partner_id,
                    tx_values={
                        'return_url': '/shop/payment/validate',
                    },
                    context=render_ctx)
        #vips_shop
        return request.website.render("vips_shop.payment", values)


    #@http.route(['/vips_shop/quick_order'], type='http', auth="public", methods=['GET'], website=True)
    @http.route(['/vips_shop/quick_order'], type='json', auth='public', website=True)
    def quick_order(self, product_id, order_description,  **kw):  #add_qty=1, set_qty=0,
        cr, uid, context, registry = request.cr, request.uid, request.context, request.registry
        add_qty=1
        set_qty=0
        _logger.info('quick_order')
        _logger.error("!!!=> getting data product_id: %r, shipping_id: %r, delivery_product_id: %r", product_id,
                      kw['shipping_id'], kw['delivery_product_id'])
        orm_quick_order = request.env['vips_shop.quick_sale_order']
        orm_partner = request.env['res.partner']

        orm_country = request.env['res.country']
        orm_delivery = request.env['vips_shop.delivery']

        country_ids = orm_country.search([('code','=','RU')])
        countries = orm_country.browse(country_ids)

        _logger.error("----> Rcived kw['shipping_id']: %r", kw['shipping_id'])
        #shipping_id = orm_delivery.sudo().browse(int(kw['shipping_id'])).product_id.id
        shipping_id = orm_delivery.sudo().browse(int(kw['delivery_product_id']))
        _logger.error("----> shipping_id: %r", shipping_id)

        # делаем ордер заказа и добавляем сразу же продукт быстрого заказа
        try:
            #_logger.info('create sale order')
            #_logger.error("request.website.sale_get_order(force_create=1) after that ---> ._cart_update(product_id=int( %r ), add_qty=float( %r ), set_qty=float( %r ))", product_id, add_qty, set_qty)
            request.website.sale_get_order(force_create=1)._cart_update(product_id=int(product_id), add_qty=float(add_qty), set_qty=float(set_qty))
        except:
            _logger.error('Error while register new order via quick_order()')
            _logger.error("request.website.sale_get_order(force_create=1) after that ---> ._cart_update(product_id=int( %r ), add_qty=float( %r ), set_qty=float( %r ))", product_id, add_qty, set_qty)
            return {'error':'error'}

        #_logger.info('get sale order')
        sale_order = request.website.sale_get_order(context=context)
        sale_order._cart_update(product_id=int(shipping_id), add_qty=float(add_qty), set_qty=float(set_qty))
        _logger.info("sale order ID: %r, partner_id: %r , order_description : %r", sale_order.id,
                     sale_order.partner_shipping_id.id, order_description)
        quick_order = orm_quick_order.create({
            'order_id':sale_order.id,
            'partner_id':sale_order.partner_shipping_id.id,
            'description': order_description
        })
        name_quick_order = 'БЗ/' + str(quick_order.id)
        quick_order.write({'name': name_quick_order})

        # gen data for create partner
        #self.checkout_form_save(values["checkout"])
        partner_name = kw['qos_name'] + ' ' +  kw['qos_surname']
        partner_info = {
            'customer': True,
            'name': partner_name,
            'display_name': partner_name,
            'street': '',
            'street2': 'Уточнить',
            'city': 'Москва',
            'email': kw['qos_email'],
            'phone': kw['qos_phone'],
            'country_id': int(countries[0].id)

        }

        _logger.info("PARTNER_INFO : %r", partner_info)
        # create partner
        partner_id = orm_partner.sudo().create(partner_info).id

        sale_value = {
            'partner_invoice_id': partner_id,
            'partner_id': partner_id,
            'usersess': request.session['webcalc_session_id'],
            'typeship':kw['shipping_id'],
            'shipaddr':  partner_id
        }
        _logger.info("----> sale_value: %s", sale_value)
        sale_order.write(sale_value)
        quick_order.write({'partner_id': partner_id})
        quick_order.env.cr.commit()
        sale_order.env.cr.commit()
        so_number = sale_order.name
        request.website.sale_reset(context=context)

        #return request.redirect("/")'''
        return {'error':'ok', 'saleorder': so_number}


# class VipStampWebShop(http.Controller):
#     @http.route('/vips_shop/vips_shop/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vips_shop/vips_shop/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vips_shop.listing', {
#             'root': '/vips_shop/vips_shop',
#             'objects': http.request.env['vips_shop.vips_shop'].search([]),
#         })

#     @http.route('/vips_shop/vips_shop/objects/<model("vips_shop.vips_shop"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vips_shop.object', {
#             'object': obj
#         })