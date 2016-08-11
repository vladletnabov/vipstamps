# -*- coding: utf-8 -*-

from openerp import models, fields, api
import datetime
from datetime import timedelta
#Import logger
import logging
#Get the logger
_logger = logging.getLogger(__name__)
from random import randint
import time
import requests

# class vips_vc(models.Model):
#     _name = 'vips_vc.vips_vc'

#     name = fields.Char()



class SessionVisitor(models.Model):
    _name = 'vips_vc.session'

    name=fields.Char()
    client_addr = fields.Char(string="Client IP", required=True)
    date_visit = fields.Datetime(default=fields.Datetime.now())
    date_last_check = fields.Datetime(default=fields.Datetime.now())

    target_url_ids = fields.Many2one('vips_vc.url_list', string='Target URL')
    #source_url_ids = fields.Many2one('vips_vc.url_list', string='Source URL')

    # тип ресурса(url_source_engine_id): поисковая машина, локальный, реклама
    # url_source_engine_id  = fields.One2many('vips_vc.search_engine', 'url_list_ids', string='Type of source')
    #site_trip_id = fields.One2many('vips_vc.site_trip', 'session_ids', string='Trip records')
    #site_trip_id = fields.Many2one('vips_vc.site_trip', string='Trip records')
    site_trip_id = fields.One2many('vips_vc.site_trip','session_ids', string='Trip records')

    #search
    #search_engine_id = fields.One2many('vips_vc.search_engine', 'session_ids', string='Search engine')
    search_engine_id = fields.Many2one('vips_vc.search_engine', string='Search engine ID')
    #search_phrase_id = fields.One2many('vips_vc.search_phrases', 'session_ids', string='Search phrase')
    search_phrase_id = fields.Many2one('vips_vc.search_phrases', string='Search phrase ID')

    # advert
    #advert_company_id = fields.One2many('vips_vc.advert_company', 'session_ids', string='Advertising company')
    #advert_engine_id = fields.One2many('vips_vc.advert_engine', 'session_ids', string='Advertising engine')
    advert_company_id = fields.Many2one('vips_vc.advert_company', string='Advertising company')
    advert_engine_id = fields.Many2one('vips_vc.advert_engine', string='Advertising engine')

class URLList(models.Model):
    _name = 'vips_vc.url_list'

    name = fields.Char(string="URL", required=True)
    url_parametes = fields.Char(string="URL parameters") #пераметры URLб всё что идёт после ?

    target_session_id = fields.One2many('vips_vc.session', 'target_url_ids', string='Target URL')
    #source_session_id = fields.One2many('vips_vc.session', 'source_url_ids', string='Source URL')

    site_trip_prevouse_id = fields.One2many('vips_vc.site_trip', 'url_prevouse_ids', string='Prevouse URL')
    site_trip_current_id  = fields.One2many('vips_vc.site_trip', 'url_current_ids',  string='Current URL')

    #site_trip_prevouse_id = fields.Many2many('vips_vc.site_trip', 'vips_vc_trip_to_prev_url_id_ref',
    #                                    'site_trip_prevouse_id','url_prevouse_ids', string='Prevouse URL')
    #site_trip_current_id  = fields.Many2many('vips_vc.site_trip', 'vips_vc_trip_to_curr_url_id_ref',
    #                                    'site_trip_current_id', 'url_current_ids',  string='Current URL')


    remote_sites_id = fields.One2many('vips_vc.remote_sites', 'site_url_ids', string='Remote site page with URL')
    remote_sites_target_url_id = fields.One2many('vips_vc.remote_sites', 'target_url_ids', string='URL on remote site page')


    #def url_exist(self, cr, SUPERUSER_ID, urlForCheck):
    #    _logger.error("Check URL exist in DB ")
    #    result = False
    #    if (self.search_count(cr, SUPERUSER_ID, [('url', '=', urlForCheck)])>0):
    #        result = True
    #    return result


class SessionTimeParameterValue(models.Model):
    _name = 'vips_vc.session_time_parameter_value'
    name = fields.Char(string="Parameter name", required=True)
    value = fields.Integer(string="Parameter value", required=True)
    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "The parameter name must be unique"),
    ]
# класс для поисковых машин
class SearchEngine(models.Model):
    _name = 'vips_vc.search_engine'
    name = fields.Char(string="Engine name", required=True)
    uniq_part_in_host = fields.Char(string="Uniq part hostname", required=True)
    search_marker = fields.Char(string="marker for search phrase", required=True) # q='' для Google, text='' для Яндекс
    #utm_marker = fields.Char(string="UTM mark name", required=True)
    #url_list_ids = fields.Many2one('vips_vc.url_list', string='Target URL')
    session_ids = fields.One2many('vips_vc.session', 'search_engine_id', string='Session IDs')

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "The parameter name must be unique"),
        ('uniq_part_in_host_unique',
         'UNIQUE(uniq_part_in_host)',
         "The parameter uniq_part_in_host must be unique"),
    ]
# класс для регистрации перемещений по сайту
class SiteTrip(models.Model):
    _name = 'vips_vc.site_trip'

    name = fields.Char()
    #session_ids = fields.Many2one('vips_vc.session', string='Session ID', index=True)
    session_ids = fields.Many2one('vips_vc.session', string='Session ID', index=True)
    url_prevouse_ids = fields.Many2one('vips_vc.url_list', string='Prevouse URL')
    url_current_ids  = fields.Many2one('vips_vc.url_list', string='Current URL')
    #url_prevouse_ids = fields.Many2many('vips_vc.url_list', 'vips_vc_trip_to_prev_url_id_ref', 'url_prevouse_ids',
    #                                    'site_trip_prevouse_id', string='Prevouse URL', index=True)
    #url_current_ids  = fields.Many2many('vips_vc.url_list','vips_vc_trip_to_curr_url_id_ref', 'url_current_ids',
    #                                    'site_trip_current_id', string='Current URL')



class VisitorPrameters(models.Model):
    _name = 'vips_vc.visitor_parameters'

    # session_id
    # from_url_id
    # search_engine_id
    # search_phrase_id


# класс для поисковых фраз
class SearchPhrases(models.Model):
    _name = 'vips_vc.search_phrases'

    name = fields.Char(string="Search phrase", required=True)
    session_ids = fields.One2many('vips_vc.session', 'search_phrase_id', string='Session IDs')

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "The parameter name must be unique"),
    ]

# класс для рекламных компаний
class AdvertCompany(models.Model):
    _name = 'vips_vc.advert_company'

    name = fields.Char(string="Company name", required=True)
    session_ids = fields.Many2one('vips_vc.session', string='Session IDs')
    #advert_engine_ids = fields.One2many('vips_vc.advert_engine', 'advert_company_id', string='Engine IDs')
    advert_engine_ids = fields.Many2one('vips_vc.advert_engine', string='Engine IDs')
    uniq_link_id = fields.One2many('vips_vc.uniq_link_id_advert', 'company_ids',
                                        string='Uniq link for advertising company')

# класс для рекламных машин
class AdvertEngine(models.Model):
    _name = 'vips_vc.advert_engine'

    name = fields.Char(string="Advertesing engine name", required=True)
    utm_source = fields.Char(string="UTM source label value") #utm_source='google' or utm_source='yandex'
    #utm_company = fields.Char(string="UTM company label value")
    utm_uniqid = fields.Char(string="UTM uniq ID label name")

    session_ids = fields.One2many('vips_vc.session', 'advert_engine_id', string='Session IDs')
    advert_company_id = fields.One2many('vips_vc.advert_company', 'advert_engine_ids',
                                        string='Advertising company')

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "The parameter name must be unique"),
    ]


class RemoteSites(models.Model):
    _name = 'vips_vc.remote_sites'

    name =  fields.One2many('vips_vc.site_list', 'remote_sites_ids', string='Site')
    site_url_ids = fields.Many2one('vips_vc.url_list', string='URL page ')
    target_url_ids = fields.Many2one('vips_vc.url_list', string='URL target page')

class SiteList(models.Model):
    _name = 'vips_vc.site_list'

    name = fields.Char(string="Site URL", required=True)
    remote_sites_ids = fields.Many2one('vips_vc.remote_sites', string='Remote site IDs')


class UniqLinkIDadvert(models.Model):
    _name = 'vips_vc.uniq_link_id_advert'

    name = fields.Char(string="Site URL", required=True)
    company_ids = fields.Many2one('vips_vc.advert_company', string='Company IDs')


