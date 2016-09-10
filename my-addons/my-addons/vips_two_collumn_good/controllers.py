# -*- coding: utf-8 -*-
from openerp import http

# class VipsTwoCollumnGood(http.Controller):
#     @http.route('/vips_two_collumn_good/vips_two_collumn_good/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vips_two_collumn_good/vips_two_collumn_good/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vips_two_collumn_good.listing', {
#             'root': '/vips_two_collumn_good/vips_two_collumn_good',
#             'objects': http.request.env['vips_two_collumn_good.vips_two_collumn_good'].search([]),
#         })

#     @http.route('/vips_two_collumn_good/vips_two_collumn_good/objects/<model("vips_two_collumn_good.vips_two_collumn_good"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vips_two_collumn_good.object', {
#             'object': obj
#         })