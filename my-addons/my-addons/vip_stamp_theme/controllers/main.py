# -*- coding: utf-8 -*-
import werkzeug

from openerp import SUPERUSER_ID
from openerp import http
from openerp.http import request
from openerp.tools.translate import _
from openerp.addons.website.models.website import slug
from openerp.addons.web.controllers.main import login_redirect


class my_theme (http.Controller):
    @http.route(['/mythemesupper/ret'], type='json', auth="public")
    def change_size(self):
        return {'x': 111111111, 'y': 2}

