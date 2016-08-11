# -*- coding: utf-8 -*-
from openerp import http

# class VipStampButtonLinks(http.Controller):
#     @http.route('/vip_stamp_button_links/vip_stamp_button_links/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vip_stamp_button_links/vip_stamp_button_links/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vip_stamp_button_links.listing', {
#             'root': '/vip_stamp_button_links/vip_stamp_button_links',
#             'objects': http.request.env['vip_stamp_button_links.vip_stamp_button_links'].search([]),
#         })

#     @http.route('/vip_stamp_button_links/vip_stamp_button_links/objects/<model("vip_stamp_button_links.vip_stamp_button_links"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vip_stamp_button_links.object', {
#             'object': obj
#         })