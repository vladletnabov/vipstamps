# -*- coding: utf-8 -*-
from openerp import fields, models

class vips_vc_session(models.Model):
    _inherit = 'vips_vc.session'
    
    
    order_id = fields.One2many('sale.order', 'usersess',string="Session customer", readonly=False)
