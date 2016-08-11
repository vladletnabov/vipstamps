# -*- coding: utf-8 -*-
from openerp import http

# class VipStampSlider(http.Controller):
#     @http.route('/vip_stamp_slider/vip_stamp_slider/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vip_stamp_slider/vip_stamp_slider/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vip_stamp_slider.listing', {
#             'root': '/vip_stamp_slider/vip_stamp_slider',
#             'objects': http.request.env['vip_stamp_slider.vip_stamp_slider'].search([]),
#         })

#     @http.route('/vip_stamp_slider/vip_stamp_slider/objects/<model("vip_stamp_slider.vip_stamp_slider"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vip_stamp_slider.object', {
#             'object': obj
#         })