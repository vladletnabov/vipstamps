# -*- coding: utf-8 -*-
from openerp import http

# class VipStampBestGoods(http.Controller):
#     @http.route('/vip_stamp_best_goods/vip_stamp_best_goods/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vip_stamp_best_goods/vip_stamp_best_goods/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vip_stamp_best_goods.listing', {
#             'root': '/vip_stamp_best_goods/vip_stamp_best_goods',
#             'objects': http.request.env['vip_stamp_best_goods.vip_stamp_best_goods'].search([]),
#         })

#     @http.route('/vip_stamp_best_goods/vip_stamp_best_goods/objects/<model("vip_stamp_best_goods.vip_stamp_best_goods"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vip_stamp_best_goods.object', {
#             'object': obj
#         })