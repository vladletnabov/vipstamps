# -*- coding: utf-8 -*-
from openerp import http

# class VipStampVideo(http.Controller):
#     @http.route('/vip_stamp_video/vip_stamp_video/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vip_stamp_video/vip_stamp_video/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vip_stamp_video.listing', {
#             'root': '/vip_stamp_video/vip_stamp_video',
#             'objects': http.request.env['vip_stamp_video.vip_stamp_video'].search([]),
#         })

#     @http.route('/vip_stamp_video/vip_stamp_video/objects/<model("vip_stamp_video.vip_stamp_video"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vip_stamp_video.object', {
#             'object': obj
#         })